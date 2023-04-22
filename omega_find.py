""" Written by Benjamin Jack Cullen
"""
import os
import sys
import time
import asyncio
import aiomultiprocess
import multiprocessing

import omega_find_sysargv

import handler_print
import handler_dict
import handler_chunk
import handler_file
import handler_results
import handler_post_process
import handler_strings
import scanfs

import async_learn
import async_contents_scan
import async_descan
import async_typescan
import async_pscan
import async_revealscan
import async_mtimescan

import variable_paths

debug = False
program_root = variable_paths.get_executable_path()


async def main(_chunks: list, _multiproc_dict: dict, _mode: str):
    async with aiomultiprocess.Pool() as pool:
        if mode == '-l':
            _results = await pool.map(async_learn.entry_point_learn, _chunks, _multiproc_dict)
        elif mode == '-c':
            _results = await pool.map(async_contents_scan.entry_point_contents_scan, _chunks, _multiproc_dict)
        elif mode == '-d':
            _results = await pool.map(async_descan.entry_point_de_scan, _chunks, _multiproc_dict)
        elif mode == '-t':
            _results = await pool.map(async_typescan.entry_point_type_scan, _chunks, _multiproc_dict)
        elif mode == '-p':
            _results = await pool.map(async_pscan.entry_point_p_scan, _chunks, _multiproc_dict)
        elif mode == '-r':
            _results = await pool.map(async_revealscan.entry_point_reveal_scan, _chunks, _multiproc_dict)
        elif mode == '-m':
            _results = await pool.map(async_mtimescan.entry_point_mtime_scan, _chunks, _multiproc_dict)
    return _results


if __name__ == '__main__':

    # used for compile time
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # get input
    STDIN = list(sys.argv)

    # check these arguments before continuing
    verbose = omega_find_sysargv.verbosity(STDIN)
    interact = omega_find_sysargv.interactive(STDIN)

    if '-h' not in STDIN:
        handler_print.display_spacer()
        handler_print.display_spacer()

    # check for light requests.
    if omega_find_sysargv.run_and_exit(stdin=STDIN, interact=interact) is False:
        # WARNING: ensure sufficient ram/page-file/swap if changing buffer_max. ensure chunk_max suits your system.
        mode, learn_bool, de_scan_bool, type_scan_bool, p_scan_bool, type_suffix, reveal_scan_bool,\
            contents_scan, mtime_scan = omega_find_sysargv.mode(STDIN)

        if type_scan_bool is True and not len(type_suffix) >= 1:
            sys.exit('-- unspecified suffix(s).\n')

        else:
            target = omega_find_sysargv.target(STDIN, mode)
            recursive = omega_find_sysargv.recursive(STDIN)
            chunk_max = omega_find_sysargv.chunk_max(STDIN)
            buffer_max = omega_find_sysargv.buffer_max(STDIN)
            db_recognized_files = omega_find_sysargv.database(STDIN)
            extract = omega_find_sysargv.extract(STDIN)
            query = omega_find_sysargv.query(STDIN)
            sort_mode = omega_find_sysargv.sort_mode(STDIN)
            write_bool = omega_find_sysargv.write_bool(STDIN)
            _digits = omega_find_sysargv.sub_digits(STDIN)

            if os.path.exists(target) and os.path.exists(db_recognized_files):

                # datetime used for timestamping files/directories
                dt = handler_strings.get_dt()

                # read recognized files
                recognized_files, suffixes = [], []
                if p_scan_bool is False or reveal_scan_bool is False or contents_scan is False:
                    recognized_files, suffixes = handler_file.db_read_handler(_learn_bool=learn_bool,
                                                                              _de_scan_bool=de_scan_bool,
                                                                              _type_scan_bool=type_scan_bool,
                                                                              _db_recognized_files=db_recognized_files,
                                                                              _type_suffix=type_suffix,
                                                                              _digits=_digits)

                # print(recognized_files)

                # pre-scan
                files, x_files, pre_scan_time = [], [], int(0)
                if os.path.isdir(target):
                    files, x_files, pre_scan_time = scanfs.pre_scan_handler(_target=target, _verbose=verbose, _recursive=recursive)
                elif os.path.isfile(target):
                    files = [target]

                if write_bool is True:
                    asyncio.run(handler_file.write_scan_results(*files, file='pre_scan_files_'+dt+'.txt', _dt=dt))
                    asyncio.run(handler_file.write_exception_log(*x_files, file='pre_scan_exception_log_'+dt+'.txt', _dt=dt))

                # chunk data ready for async multiprocess
                chunks = handler_chunk.chunk_data(files, chunk_max)

                # developer view (replace verbose here with a --debug switch)
                # if verbose is True:
                #     print(f'[CHUNKS]')
                #     for chunk in chunks:
                #         print(chunk)

                # prepare a dictionary for each child process (requires my modified aiomultiprocess pool.py)
                multiproc_dict = handler_dict.dict_maker(_recognized_files=recognized_files,
                                                         _buffer_max=buffer_max,
                                                         _type_suffix=type_suffix, _learn=learn_bool,
                                                         _de_scan=de_scan_bool, _type_scan=type_scan_bool,
                                                         _p_scan=p_scan_bool,
                                                         _extract=extract, _target=target, _reveal_scan=reveal_scan_bool,
                                                         _program_root=program_root,
                                                         _contents_scan=contents_scan, _query=query,
                                                         _verbose=verbose,
                                                         _digits=_digits)

                # run the async multiprocess operation(s)
                t = time.perf_counter()
                results = asyncio.run(main(chunks, multiproc_dict, mode))
                t_completion = str(time.perf_counter()-t)
                results = handler_chunk.un_chunk_data(results, depth=1)
                # print('final results:')
                # for result in results:
                #     print(result)
                exc, results = handler_post_process.results_filter(results)

                if write_bool is True:
                    asyncio.run(handler_file.write_exception_log(*exc, file='exception_log_' + dt + '.txt', _dt=dt))

                # post-processing
                if p_scan_bool is True:
                    results = asyncio.run(handler_post_process.pscan(_list=results))
                elif de_scan_bool is True and extract is True:
                    results = handler_post_process.descan(_list=results, _recognized_files=recognized_files)
                elif contents_scan is True and extract is True:
                    # results = asyncio.run(handler_post_process.cscan(_list=results))
                    results = handler_chunk.un_chunk_data(results, depth=1)

                if learn_bool is False and mtime_scan is False:
                    # sort
                    if sort_mode == '--sort=mtime':
                        results = sorted(results, key=lambda x: x[0])
                    elif sort_mode == '--sort=buffer':
                        results = sorted(results, key=lambda x: x[1])
                    elif sort_mode == '--sort=size':
                        results = sorted(results, key=lambda x: x[2])
                    elif sort_mode == '--sort=file':
                        results = sorted(results, key=lambda x: x[3])

                    elif sort_mode == '--sort-reverse=mtime':
                        results = sorted(results, key=lambda x: x[0], reverse=True)
                    elif sort_mode == '--sort-reverse=buffer':
                        results = sorted(results, key=lambda x: x[1], reverse=True)
                    elif sort_mode == '--sort-reverse=size':
                        results = sorted(results, key=lambda x: x[2], reverse=True)
                    elif sort_mode == '--sort-reverse=file':
                        results = sorted(results, key=lambda x: x[3], reverse=True)

                # sort
                elif mtime_scan is True:
                    if sort_mode == '--sort=mtime':
                        results = sorted(results, key=lambda x: x[0])
                    elif sort_mode == '--sort=size':
                        results = sorted(results, key=lambda x: x[1])
                    elif sort_mode == '--sort=file':
                        results = sorted(results, key=lambda x: x[2])

                    elif sort_mode == '--sort-reverse=mtime':
                        results = sorted(results, key=lambda x: x[0], reverse=True)
                    elif sort_mode == '--sort-reverse=size':
                        results = sorted(results, key=lambda x: x[1], reverse=True)
                    elif sort_mode == '--sort-reverse=file':
                        results = sorted(results, key=lambda x: x[2], reverse=True)

                # post-scan results
                handler_results.post_scan_results(_results=results, _db_recognized_files=db_recognized_files,
                                                  _learn_bool=learn_bool, _de_scan_bool=de_scan_bool,
                                                  _type_scan_bool=type_scan_bool, _p_scan=p_scan_bool,
                                                  _dt=dt, _exc=exc, _reveal_scan=reveal_scan_bool,
                                                  _t_completion=t_completion, _extract=extract, _verbose=verbose,
                                                  _pre_scan_time=pre_scan_time, interact=interact,
                                                  _contents_scan=contents_scan, _query=query, write_bool=write_bool,
                                                  _mtime_scan=mtime_scan)

                # final clean of tmp
                if os.path.exists(variable_paths.tmp_dir_path):
                    handler_file.rem_dir(path=variable_paths.tmp_dir_path)

            else:
                handler_print.display_invalid_input()
                if not os.path.exists(target):
                    handler_print.display_invalid_path(target)

                if not os.path.exists(db_recognized_files):
                    handler_print.display_invalid_database(db_recognized_files)

                handler_print.omega_help()

    handler_print.display_spacer()
    handler_print.display_spacer()
