""" Written by Benjamin Jack Cullen
Intention: De-Obfuscation.
Setup: Multiprocess + Async.
"""
import os
import sys
import re
import time
import string
import random
from datetime import datetime
import asyncio
import aiomultiprocess
import multiprocessing

import handler_dict
import handler_chunk
import handler_file
import handler_results
import handler_exception
import omega_find_banner
import omega_find_help
import omega_find_sysargv
import post_process
import scanfs
import get_path

debug = False
x_learn = []

program_root = get_path.get_path()


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def randStr(chars=string.ascii_uppercase + string.digits, n=32) -> str:
    return ''.join(random.choice(chars) for _ in range(n))


def sub_str(_buffer: bytes) -> str:
    digi_str = r'[0-9]'
    return re.sub(digi_str, '', str(_buffer))


async def check_extract(_extract: bool, _buffer: bytes) -> bool:
    if _extract is True:
        _buffer = str(_buffer).strip()
        return True


async def extract_de_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list, _target: str) -> list:
    _results = [[_file, _buffer]]
    _tmp = program_root+'\\tmp\\'+str(randStr())
    result_bool, extraction = await asyncio.to_thread(handler_file.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        if os.path.exists(_tmp):
            sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
            sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
            for sub_file in sub_files:
                buffer = await handler_file.async_read_bytes(sub_file, _buffer_max)
                suffix = await asyncio.to_thread(handler_file.get_suffix, sub_file)
                res = await de_scan_check(sub_file, suffix, buffer, _recognized_files)
                if res is not None:
                    res[0] = res[0].replace(_tmp, _target)
                    _results.append(res)
    else:
        _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results


async def extract_type_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list,
                            _type_suffix: list, _target: str) -> list:
    _results = [[_file, _buffer]]
    _tmp = program_root+'\\tmp\\'+str(randStr())
    result_bool, extraction = await asyncio.to_thread(handler_file.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
        sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
        for sub_file in sub_files:
            buffer = await handler_file.async_read_bytes(sub_file, _buffer_max)
            suffix = await asyncio.to_thread(handler_file.get_suffix, sub_file)
            res = await type_scan_check(sub_file, suffix, buffer, _recognized_files, _type_suffix)
            if res is not None:
                res[0] = res[0].replace(_tmp, _target)
                _results.append(res)
    else:
        _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results


async def extract_p_scan(_buffer: bytes, _file: str, _buffer_max: int, _target: str) -> list:
    _result = [_file]
    _tmp = program_root+'\\tmp\\'+str(randStr())
    _result_bool, _results = await asyncio.to_thread(handler_file.extract_nested_compressed,
                                                     file=_file,
                                                     temp_directory=_tmp,
                                                     _target=_target,
                                                     _static_tmp=_tmp)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    final_res = []
    for res in _results:
        if 'Password required' in res:
            if res not in final_res:
                final_res.append(res)
        elif res[0] == '[ERROR]':
            if res not in final_res:
                final_res.append(res)
    return final_res


async def extract_reveal_scan(_buffer: bytes, _file: str, _buffer_max: int, _target: str) -> list:
    _results = [_file, _buffer]
    _tmp = program_root+'\\tmp\\'+str(randStr())
    result_bool, extraction = await asyncio.to_thread(handler_file.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
        sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
        for sub_file in sub_files:
            buffer = await handler_file.async_read_bytes(sub_file, _buffer_max)
            res = [sub_file, buffer]
            if res is not None:
                res[0] = res[0].replace(_tmp, _target)
                _results.append(res)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results


async def scan_learn_check(suffix: str, buffer: bytes, _recognized_files: list) -> list:
    global x_learn
    buffer = sub_str(_buffer=buffer)
    if [suffix, buffer] not in x_learn:
        x_learn.append([suffix, buffer])
        if [suffix, buffer] not in _recognized_files:
            return [suffix, buffer]


async def de_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    buffer = sub_str(_buffer=buffer)
    if [suffix, buffer] not in _recognized_files:
        return [file, suffix, buffer]


async def type_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list, _type_suffix: list):
    buffer = sub_str(_buffer=buffer)
    if [buffer] in _recognized_files:
        return [file, suffix, buffer]


async def scan_learn(file: str, _recognized_files: list, _buffer_max: int) -> list:
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await scan_learn_check(suffix, buffer, _recognized_files)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def de_scan(file: str, _recognized_files: list, _buffer_max: int, _extract: bool, _target: str) -> list:
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await de_scan_check(file, suffix, buffer, _recognized_files)
        if await check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_de_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max,
                                            _recognized_files=_recognized_files, _target=_target)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def type_scan(file: str, _recognized_files: list, _buffer_max: int, _type_suffix: list, _extract: bool, _target: str):
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await type_scan_check(file, suffix, buffer, _recognized_files, _type_suffix)
        if await check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_type_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max,
                                              _recognized_files=_recognized_files, _type_suffix=_type_suffix,
                                              _target=_target)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def p_scan(file: str, _buffer_max: int, _extract: bool, _target: str) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        if await check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_p_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max, _target=_target)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def reveal_scan(file: str, _buffer_max: int, _extract: bool, _target: str) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        _result = [file, buffer]
        if await check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_reveal_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max, _target=_target)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await scan_learn(item, _recognized_files, _buffer_max) for item in chunk]


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _extract = False
    if 'extract' in kwargs.keys():
        _extract = kwargs.get('extract')
    return [await de_scan(item, _recognized_files, _buffer_max, _extract, _target) for item in chunk]


async def entry_point_type_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _type_suffix = kwargs.get('suffix')
    _target = str(kwargs.get('target'))
    _extract = False
    if 'extract' in kwargs.keys():
        _extract = kwargs.get('extract')
    return [await type_scan(item, _recognized_files, _buffer_max, _type_suffix, _extract, _target) for item in chunk]


async def entry_point_p_scan(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    return [await p_scan(item, _buffer_max, _extract=True, _target=_target) for item in chunk]


async def entry_point_reveal_scan(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _extract = False
    if 'extract' in kwargs.keys():
        _extract = kwargs.get('extract')
    return [await reveal_scan(item, _buffer_max, _extract, _target) for item in chunk]


async def main(_chunks: list, _multiproc_dict: dict, _mode: str):
    async with aiomultiprocess.Pool() as pool:
        if mode == '-l':
            _results = await pool.map(entry_point_learn, _chunks, _multiproc_dict)
        elif mode == '-d':
            _results = await pool.map(entry_point_de_scan, _chunks, _multiproc_dict)
        elif mode == '-t':
            _results = await pool.map(entry_point_type_scan, _chunks, _multiproc_dict)
        elif mode == '-p':
            _results = await pool.map(entry_point_p_scan, _chunks, _multiproc_dict)
        elif mode == '-r':
            _results = await pool.map(entry_point_reveal_scan, _chunks, _multiproc_dict)
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
            dt = get_dt()

            # read recognized files
            recognized_files, suffixes = [], []
            if p_scan_bool is False or reveal_scan_bool is False:
                recognized_files, suffixes = handler_file.db_read_handler(_learn_bool=learn_bool,
                                                                          _de_scan_bool=de_scan_bool,
                                                                          _type_scan_bool=type_scan_bool,
                                                                          _db_recognized_files=db_recognized_files,
                                                                          _type_suffix=type_suffix)
            # pre-scan
            files, x_files = handler_file.pre_scan_handler(_target=target)
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
            exc, results = handler_exception.results_filter(results)
            asyncio.run(handler_file.write_exception_log(*exc, file='exception_log_' + dt + '.txt', _dt=dt))

            # post-processing
            if p_scan_bool is True:
                results = post_process.pscan(_list=results)

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
