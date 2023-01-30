""" Written by Benjamin Jack Cullen
Intention: De-Obfuscation.
Setup: Multiprocess + Async.
"""
import os
import sys
import re
import time
from datetime import datetime
import asyncio
import aiofiles
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
import scanfs
import shutil
import string
import random

debug = False
x_learn = []


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def randStr(chars=string.ascii_uppercase + string.digits, n=32) -> str:
    return ''.join(random.choice(chars) for _ in range(n))


async def extract_type_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list,
                            _type_suffix: list) -> list:
    _result = [_file]
    _tmp = '.\\tmp\\'+str(randStr())+'\\'
    extraction = handler_file.extract_nested_compressed(file=_file, temp_directory=_tmp)
    if extraction is True:
        sub_files = scanfs.scan(_tmp)
        sub_files = handler_chunk.un_chunk_data(sub_files, depth=1)
        for sub_file in sub_files:
            buffer = await read_bytes(sub_file, _buffer_max)
            suffix = await asyncio.to_thread(handler_file.get_suffix, sub_file)
            _result.append(await type_scan_check(sub_file, suffix, buffer, _recognized_files, _type_suffix))
        shutil.rmtree(_tmp)
    else:
        _result = extraction
    return _result


async def extract_de_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list) -> list:
    _result = [_file]
    _tmp = '.\\tmp\\'+str(randStr())+'\\'
    extraction = handler_file.extract_nested_compressed(file=_file, temp_directory=_tmp)
    if extraction is True:
        sub_files = scanfs.scan(_tmp)
        sub_files = handler_chunk.un_chunk_data(sub_files, depth=1)
        for sub_file in sub_files:
            buffer = await read_bytes(sub_file, _buffer_max)
            suffix = await asyncio.to_thread(handler_file.get_suffix, sub_file)
            _result.append(await de_scan_check(sub_file, suffix, buffer, _recognized_files))
        shutil.rmtree(_tmp)
    else:
        _result = extraction
    return _result


async def check_extract(_extract: bool, _buffer: bytes) -> bool:
    if _extract is True:
        if 'Zip archive' in str(_buffer) or '7-zip archive' in str(_buffer):
            return True


async def read_bytes(file: str, _buffer_max: int) -> bytes:
    async with aiofiles.open(file, mode='rb') as handle:
        _bytes = await handle.read(_buffer_max)
        await handle.close()
    return await asyncio.to_thread(handler_file.file_sub_ops, _bytes)


async def de_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    digi_str = r'[0-9]'
    buffer = re.sub(digi_str, '', str(buffer))
    if [suffix, buffer] not in _recognized_files:
        return [file, suffix, buffer]


async def de_scan(file: str, _recognized_files: list, _buffer_max: int, _extract: bool) -> list:
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await de_scan_check(file, suffix, buffer, _recognized_files)
        if await check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_de_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max,
                                            _recognized_files=_recognized_files)
    except Exception as e:
        _result = handler_exception.exception_format(e)
    return _result


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _extract = False
    if 'extract' in kwargs.keys():
        _extract = kwargs.get('extract')
    return [await de_scan(item, _recognized_files, _buffer_max, _extract) for item in chunk]


async def type_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list, _type_suffix: list):
    digi_str = r'[0-9]'
    buffer = re.sub(digi_str, '', str(buffer))
    if [buffer] in _recognized_files:
        return [file, suffix, buffer]


async def type_scan(file: str, _recognized_files: list, _buffer_max: int, _type_suffix: list, _extract: bool):
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await type_scan_check(file, suffix, buffer, _recognized_files, _type_suffix)
        if await check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_type_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max,
                                              _recognized_files=_recognized_files, _type_suffix=_type_suffix)
    except Exception as e:
        _result = handler_exception.exception_format(e)
    return _result


async def scan_learn_check(suffix: str, buffer: bytes, _recognized_files: list) -> list:
    global x_learn
    digi_str = r'[0-9]'
    buffer = re.sub(digi_str, '', str(buffer))
    if [suffix, buffer] not in x_learn:
        x_learn.append([suffix, buffer])
        if [suffix, buffer] not in _recognized_files:
            return [suffix, buffer]


async def scan_learn(file: str, _recognized_files: list, _buffer_max: int) -> list:
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await scan_learn_check(suffix, buffer, _recognized_files)
    except Exception as e:
        _result = handler_exception.exception_format(e)
    return _result


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await scan_learn(item, _recognized_files, _buffer_max) for item in chunk]


async def entry_point_type_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _type_suffix = kwargs.get('suffix')
    _extract = False
    if 'extract' in kwargs.keys():
        _extract = kwargs.get('extract')
    return [await type_scan(item, _recognized_files, _buffer_max, _type_suffix, _extract) for item in chunk]


async def main(_chunks: list, _multiproc_dict: dict, _mode: str):
    async with aiomultiprocess.Pool() as pool:
        if mode == '--learn':
            _results = await pool.map(entry_point_learn, _chunks, _multiproc_dict)
        elif mode == '--de-scan':
            _results = await pool.map(entry_point_de_scan, _chunks, _multiproc_dict)
        elif mode == '--type-scan':
            _results = await pool.map(entry_point_type_scan, _chunks, _multiproc_dict)
    return _results


if __name__ == '__main__':

    # used for compile time
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # get input
    STDIN = list(sys.argv)

    # check for light requests.
    if omega_find_sysargv.run_and_exit(stdin=STDIN) is False:

        # WARNING: ensure sufficient ram/page-file/swap if changing buffer_max. ensure chunk_max suits your system.
        mode, learn_bool, de_scan_bool, type_scan_bool, type_suffix = omega_find_sysargv.mode(STDIN)
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
                                                     _extract=extract)

            # run the async multiprocess operation(s)
            print('-- scanning target ...')
            t = time.perf_counter()
            results = asyncio.run(main(chunks, multiproc_dict, mode))
            print(f'-- scan time: {time.perf_counter()-t}')
            results = handler_chunk.un_chunk_data(results, depth=1)
            exc, results = handler_exception.separate_exception(results)
            print(f'-- errors: {len(exc)}')
            asyncio.run(handler_file.write_exception_log(*exc, file='exception_log_' + dt + '.txt', _dt=dt))

            # post-scan results
            handler_results.post_scan_results(_results=results, _db_recognized_files=db_recognized_files,
                                              _learn_bool=learn_bool, _de_scan_bool=de_scan_bool,
                                              _type_scan_bool=type_scan_bool, _dt=dt)

        else:
            print('-- invalid input')
            if not os.path.exists(target):
                print(f'-- invalid path: {target}')
            if not os.path.exists(db_recognized_files):
                print(f'-- invalid database: {db_recognized_files}')
            omega_find_help.omega_help()
