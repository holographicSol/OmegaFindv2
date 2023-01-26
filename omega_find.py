""" Written by Benjamin Jack Cullen
Intention: De-Obfuscation.
Setup: Multiprocess + Async.
"""
import os
import sys
import re
import time
import magic
from datetime import datetime
import pathlib
import asyncio
import aiofiles
import aiomultiprocess
import multiprocessing
import exception_handler
import omega_find_dict_maker
import chunk_handler
import omega_find_help
import omega_find_sysargv
import file_handler

debug = False
x_learn = []


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def get_suffix(file: str) -> str:
    sfx = pathlib.Path(file).suffix
    sfx = sfx.replace('.', '').lower()
    if sfx == '':
        sfx = 'no_file_extension'
    return sfx


def file_sub_ops(_bytes: bytes) -> str:
    buff = ''
    try:
        buff = magic.from_buffer(_bytes)
    except Exception as e:
        if debug is True:
            print(f'[FROM BUFFER] {e}')
    return buff


async def read_bytes(file: str, _buffer_max: int) -> bytes:
    async with aiofiles.open(file, mode='rb') as handle:
        _bytes = await handle.read(_buffer_max)
        await handle.close()
    return await asyncio.to_thread(file_sub_ops, _bytes)


async def de_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    digi_str = r'[0-9]'
    buffer = re.sub(digi_str, '', str(buffer))
    if [suffix, buffer] not in _recognized_files:
        return [file, suffix, buffer]


async def de_scan(file: str, _recognized_files: list, _buffer_max: int) -> list:
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(get_suffix, file)
        _result = await de_scan_check(file, suffix, buffer, _recognized_files)
    except Exception as e:
        _result = exception_handler.exception_format(e)
    return _result


async def type_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list, _type_suffix: list):
    digi_str = r'[0-9]'
    buffer = re.sub(digi_str, '', str(buffer))
    if [buffer] in _recognized_files:
        return [file, suffix, buffer]


async def type_scan(file: str, _recognized_files: list, _buffer_max: int, _type_suffix: list):
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(get_suffix, file)
        _result = await type_scan_check(file, suffix, buffer, _recognized_files, _type_suffix)
    except Exception as e:
        _result = exception_handler.exception_format(e)
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
        suffix = await asyncio.to_thread(get_suffix, file)
        _result = await scan_learn_check(suffix, buffer, _recognized_files)
    except Exception as e:
        _result = exception_handler.exception_format(e)
    return _result


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await scan_learn(item, _recognized_files, _buffer_max) for item in chunk]


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await de_scan(item, _recognized_files, _buffer_max) for item in chunk]


async def entry_point_type_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _type_suffix = kwargs.get('suffix')
    return [await type_scan(item, _recognized_files, _buffer_max, _type_suffix) for item in chunk]


async def main(_chunks: list, _multiproc_dict: dict, _mode: str):
    async with aiomultiprocess.Pool() as pool:
        if mode == '--learn':
            _results = await pool.map(entry_point_learn, _chunks, _multiproc_dict)
        elif mode == '--de-scan':
            _results = await pool.map(entry_point_de_scan, _chunks, _multiproc_dict)
        elif mode == '--type-scan':
            _results = await pool.map(entry_point_type_scan, _chunks, _multiproc_dict)
    return _results


def result_handler(_results: list):
    if len(_results) <= 12:
        print('[Unrecognized files]:')
        for result in _results:
            print(' ', result)
    else:
        print('[Unrecognized files]:')
        i_result = 0
        for result in _results:
            if i_result <= 12:
                print(' ', result)
                i_result += 1
            else:
                break


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    STDIN = sys.argv
    STDIN = list(STDIN)

    if '-h' in STDIN:
        omega_find_help.omega_help()

    elif '--recognized' in STDIN:
        print('\n[OmegaFind v2] Multi-processed async for better performance.')
        db_recognized_files = omega_find_sysargv.display_recognized(STDIN)
        asyncio.run(file_handler.read_definitions(fname=db_recognized_files))

    elif '--new-suffix-group' in STDIN:
        print('\n[OmegaFind v2]')
        omega_find_sysargv.make_suffix_group()

    else:
        # Notice: Requires the aiomultiprocess pool file that I personally modified or this will not work.
        # WARNING: ensure sufficient ram/page-file/swap if changing buffer_max. ensure chunk_max suits your system.

        mode, learn_bool, de_scan_bool, type_scan_bool, type_suffix = omega_find_sysargv.mode(STDIN)
        target = omega_find_sysargv.target(STDIN, mode)
        chunk_max = omega_find_sysargv.chunk_max(STDIN)
        buffer_max = omega_find_sysargv.buffer_max(STDIN)
        db_recognized_files = omega_find_sysargv.database(STDIN)
        verbose = omega_find_sysargv.verbosity(STDIN)

        if os.path.exists(target) and os.path.exists(db_recognized_files):
            print('\n[OmegaFind v2] Multi-processed async for better performance.\n')

            dt = get_dt()

            # read recognized files
            recognized_files, suffixes = [], []
            if learn_bool is True or de_scan_bool is True:
                recognized_files, suffixes = asyncio.run(file_handler.read_definitions(fname=db_recognized_files))
            elif type_scan_bool is True:
                recognized_files, suffixes = asyncio.run(file_handler.read_type_definitions(fname=db_recognized_files,
                                                                                            _type_suffix=type_suffix))

            # pre-scan
            files, x_files = file_handler.pre_scan_handler(_target=target)
            asyncio.run(file_handler.write_scan_results(*files, file='pre_scan_files_'+dt+'.txt', _dt=dt))
            asyncio.run(file_handler.write_exception_log(*x_files, file='pre_scan_exception_log_'+dt+'.txt', _dt=dt))

            # chunk data ready for async multiprocess
            chunks = chunk_handler.chunk_data(files, chunk_max)

            # prepare a dictionary of useful things for each child process
            multiproc_dict = omega_find_dict_maker.dict_maker(_recognized_files=recognized_files,
                                                              _buffer_max=buffer_max,
                                                              _type_suffix=type_suffix, _learn=learn_bool,
                                                              _de_scan=de_scan_bool, _type_scan=type_scan_bool)

            # run the async multiprocess operation(s)
            print('[Scanning Target] ..')
            t = time.perf_counter()
            results = asyncio.run(main(chunks, multiproc_dict, mode))
            print(f'[Async Multi-Process Time] {time.perf_counter()-t}')
            results = chunk_handler.un_chunk_data(results, depth=1)
            exc, results = exception_handler.separate_exception(results)
            print(f'[Errors] {len(exc)}')
            asyncio.run(file_handler.write_exception_log(*exc, file='exception_log_' + dt + '.txt', _dt=dt))

            # post-scan
            if len(results) >= 1:
                if learn_bool is True:
                    print(f'[New Definitions] {len(results)}')
                    print('[Updating Definitions] ..')
                    asyncio.run(file_handler.write_definitions(*results, file=db_recognized_files))
                    asyncio.run(file_handler.clean_database(fname=db_recognized_files))
                elif de_scan_bool is True:
                    print(f'[Unrecognized Files] {len(results)}')
                    print('[Writing Scan Results] ..')
                    asyncio.run(file_handler.write_scan_results(*results, file='scan_results__'+dt+'.txt', _dt=dt))
                    result_handler(_results=results)
                elif type_scan_bool is True:
                    print(f'[Found Files] {len(results)}')
                    print('[Writing Scan Results] ..')
                    asyncio.run(file_handler.write_scan_results(*results, file='scan_results__'+dt+'.txt', _dt=dt))
            else:
                print('[Zero Results]')
            print('')

        else:
            print('[Invalid Input]')
            if not os.path.exists(target):
                print('[Invalid Target]', target)
            if not os.path.exists(db_recognized_files):
                print('[Invalid Database]', db_recognized_files)
            omega_find_help.omega_help()
