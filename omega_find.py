""" Written by Benjamin Jack Cullen
Intention: De-Obfuscation.
Setup: Multiprocess + Async.
"""
import os
import sys
import time
import asyncio
import aiomultiprocess
import multiprocessing

import omega_find_banner
import omega_find_help
import omega_find_sysargv

import handler_dict
import handler_chunk
import handler_file
import handler_results
import handler_post_process
import handler_strings
import scanfs

import async_learn
import async_descan
import async_typescan
import async_pscan
import async_revealscan

debug = False
program_root = handler_file.get_executable_path()


async def main(_chunks: list, _multiproc_dict: dict, _mode: str):
    async with aiomultiprocess.Pool() as pool:
        if mode == '-l':
            _results = await pool.map(async_learn.entry_point_learn, _chunks, _multiproc_dict)
        elif mode == '-d':
            _results = await pool.map(async_descan.entry_point_de_scan, _chunks, _multiproc_dict)
        elif mode == '-t':
            _results = await pool.map(async_typescan.entry_point_type_scan, _chunks, _multiproc_dict)
        elif mode == '-p':
            _results = await pool.map(async_pscan.entry_point_p_scan, _chunks, _multiproc_dict)
        elif mode == '-r':
            _results = await pool.map(async_revealscan.entry_point_reveal_scan, _chunks, _multiproc_dict)
    return _results


if __name__ == '__main__':

    # used for compile time
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # ensure default database file
    handler_file.ensure_db()

    # get input
    STDIN = list(sys.argv)

    # check for light requests.
    if omega_find_sysargv.run_and_exit(stdin=STDIN) is False:

        # WARNING: ensure sufficient ram/page-file/swap if changing buffer_max. ensure chunk_max suits your system.
        mode, learn_bool, de_scan_bool, type_scan_bool, p_scan_bool, type_suffix, reveal_scan_bool = omega_find_sysargv.mode(STDIN)
        if type_scan_bool is True and not len(type_suffix) >= 1:
            sys.exit('-- exiting ...\n')
        target = omega_find_sysargv.target(STDIN, mode)
        chunk_max = omega_find_sysargv.chunk_max(STDIN)
        buffer_max = omega_find_sysargv.buffer_max(STDIN)
        db_recognized_files = omega_find_sysargv.database(STDIN)
        extract = omega_find_sysargv.extract(STDIN)
        verbose = omega_find_sysargv.verbosity(STDIN)

        if os.path.exists(target) and os.path.exists(db_recognized_files):
            omega_find_banner.banner()

            # datetime used for timestamping files/directories
            dt = handler_strings.get_dt()

            # read recognized files
            recognized_files, suffixes = [], []
            if p_scan_bool is False or reveal_scan_bool is False:
                recognized_files, suffixes = handler_file.db_read_handler(_learn_bool=learn_bool,
                                                                          _de_scan_bool=de_scan_bool,
                                                                          _type_scan_bool=type_scan_bool,
                                                                          _db_recognized_files=db_recognized_files,
                                                                          _type_suffix=type_suffix)
            # pre-scan
            files, x_files = scanfs.pre_scan_handler(_target=target)
            asyncio.run(handler_file.write_scan_results(*files, file='pre_scan_files_'+dt+'.txt', _dt=dt))
            asyncio.run(handler_file.write_exception_log(*x_files, file='pre_scan_exception_log_'+dt+'.txt', _dt=dt))

            # chunk data ready for async multiprocess
            chunks = handler_chunk.chunk_data(files, chunk_max)

            # prepare a dictionary for each child process (requires my modified aiomultiprocess pool.py)
            multiproc_dict = handler_dict.dict_maker(_recognized_files=recognized_files,
                                                     _buffer_max=buffer_max,
                                                     _type_suffix=type_suffix, _learn=learn_bool,
                                                     _de_scan=de_scan_bool, _type_scan=type_scan_bool,
                                                     _p_scan=p_scan_bool,
                                                     _extract=extract, _target=target, _reveal_scan=reveal_scan_bool)

            # run the async multiprocess operation(s)
            t = time.perf_counter()
            results = asyncio.run(main(chunks, multiproc_dict, mode))
            t_completion = str(time.perf_counter()-t)
            results = handler_chunk.un_chunk_data(results, depth=1)
            exc, results = handler_post_process.results_filter(results)
            asyncio.run(handler_file.write_exception_log(*exc, file='exception_log_' + dt + '.txt', _dt=dt))

            # post-processing
            if p_scan_bool is True:
                results = handler_post_process.pscan(_list=results)

            # post-scan results
            handler_results.post_scan_results(_results=results, _db_recognized_files=db_recognized_files,
                                              _learn_bool=learn_bool, _de_scan_bool=de_scan_bool,
                                              _type_scan_bool=type_scan_bool, _p_scan=p_scan_bool,
                                              _dt=dt, _exc=exc, _reveal_scan=reveal_scan_bool,
                                              _t_completion=t_completion, _extract=extract)

            # final clean of tmp
            if os.path.exists(program_root+'\\tmp\\'):
                handler_file.rem_dir(path=program_root+'\\tmp\\')

        else:
            print('-- invalid input')
            if not os.path.exists(target):
                print(f'-- invalid path: {target}')
            if not os.path.exists(db_recognized_files):
                print(f'-- invalid database: {db_recognized_files}')
            omega_find_help.omega_help()
