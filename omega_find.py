""" Written by Benjamin Jack Cullen
Intention: De-Obfuscation.
Setup: Multiprocess + Async.
"""
import os
import sys
import time
from datetime import datetime
import magic
import codecs
import asyncio
from aiomultiprocess import Pool

import omega_find_sysargv
import prescan
import chunk_handler
import pathlib
import aiofiles
import omega_find_help
import re

learn_seen_before = []


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def pre_scan_handler(_target: str) -> list:
    scan_results = prescan.scan(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    return _files, _x_files


def read_db():
    _recognized_files, _suffixes = [], []
    if os.path.exists(_db_recognized_files):
        if learn is False:
            _recognized_files, _suffixes = asyncio.run(async_read_definitions(fname=_db_recognized_files, digits=_digits))
        elif learn is True:
            _recognized_files, _suffixes = asyncio.run(async_read_definitions_learn_mode(fname=_db_recognized_files))
    return _recognized_files, _suffixes


def get_suffix(file: str) -> str:
    sfx = pathlib.Path(file).suffix
    sfx = sfx.replace('.', '').lower()
    if sfx == '':
        sfx = 'no_file_extension'
    return sfx


def file_sub_ops(_bytes: str) -> str:
    buff = ''
    try:
        buff = magic.from_buffer(_bytes)
    except:
        pass
    return buff


async def read_bytes(file: str, _buffer_max: int) -> bytes:
    async with aiofiles.open(file, mode='rb') as handle:
        _bytes = await handle.read(_buffer_max)
        await handle.close()
    return await asyncio.to_thread(file_sub_ops, _bytes)


async def scan_learn_check(suffix: str, buffer: bytes, _recognized_files):
    global learn_seen_before
    if [suffix, buffer] not in _recognized_files:
        if [suffix, buffer] not in learn_seen_before:
            learn_seen_before.append([suffix, buffer])
            return [suffix, buffer]


async def scan_learn(file: str, _recognized_files: list, _buffer_max: int) -> list:
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(get_suffix, file)
        x = await scan_learn_check(suffix, buffer, _recognized_files)
        return x
    except:
        pass


async def de_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files, digits: False):
    tmp_buffer = buffer
    if digits is True:
        digi_str = r'[0-9]'
        tmp_buffer = re.sub(digi_str, '', str(buffer))
    if [suffix, tmp_buffer] not in _recognized_files:
        return [file, suffix, buffer]


async def de_scan(file: str, _recognized_files: list, _buffer_max: int, digits: False) -> list:
    global learn_seen_before
    try:
        buffer = await read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(get_suffix, file)
        return await de_scan_check(file, suffix, buffer, _recognized_files, digits)
    except:
        pass


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await scan_learn(item, _recognized_files, _buffer_max) for item in chunk]


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _digits = bool(kwargs.get('digits'))
    return [await de_scan(item, _recognized_files, _buffer_max, _digits) for item in chunk]


async def main(_chunks: list, _multiproc_dict: dict, _mode: str):
    global learn_seen_before
    async with Pool() as pool:
        if mode == '--learn':
            learn_seen_before = []
            _results = await pool.map(entry_point_learn, _chunks, _multiproc_dict)
        elif mode == '--de-scan':
            _results = await pool.map(entry_point_de_scan, _chunks, _multiproc_dict)
    return _results


async def async_read_definitions(fname: str, digits: False):
    async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
        _data = await handle.read()
    _data = _data.split('\n')
    _file_recognition_store = []
    _suffixes = []
    digi_str = r'[0-9]'
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        buffer = datas[idx+1:]
        if digits is True:
            buffer = re.sub(digi_str, '', buffer)
        _file_recognition_store.append([suffix, buffer])
        if suffix not in _suffixes:
            _suffixes.append(suffix)
    return _file_recognition_store, _suffixes


async def async_read_definitions_learn_mode(fname: str):
    async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
        _data = await handle.read()
    _data = _data.split('\n')
    _file_recognition_store = []
    _suffixes = []
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        buffer = datas[idx+1:]
        _file_recognition_store.append([suffix, buffer])
        if suffix not in _suffixes:
            _suffixes.append(suffix)
    return _file_recognition_store, _suffixes


async def async_write_definitions(*args, file: str):
    if not os.path.exists('./db/'):
        os.mkdir('./db/')
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg[0] + ' ' + arg[1]) for arg in args))
        await handle.write('\n')


async def async_write_scan_results(*args, file: str, _dt: str):
    target_dir = './data/' + _dt + '/'
    if not os.path.exists('./data/'):
        os.mkdir('./data/')
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    file = target_dir + file
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg) for arg in args))


if __name__ == '__main__':

    if '-h' in sys.argv:
        omega_find_help.omega_help()

    else:
        # Notice: Requires the aiomultiprocess pool file that I personally modified or this will not work.
        # WARNING: ensure sufficient ram/page-file/swap if changing buffer_max. ensure _proc_max suits your system.

        mode, learn, de_scan = omega_find_sysargv.mode()
        _target = omega_find_sysargv.target(mode)
        _proc_max = omega_find_sysargv.proc_max()
        _buffer_max = omega_find_sysargv.buffer_max()
        _db_recognized_files = omega_find_sysargv.database()
        _digits = omega_find_sysargv.digits()
        verbose = omega_find_sysargv.verbosity()

        if os.path.exists(_target):
            print('\n[OmegaFind v2] Version 2. Multi-processed async for better performance.')

            dt = get_dt()

            recognized_files, suffixes = read_db()

            if verbose is True:
                print(f'[Recognized Buffers] {len(recognized_files)}')
                print(f'[Known Suffixes] {len(suffixes)}')
                # print(recognized_files)

            # pre-scan
            print('[Pre-Scanning] ..')
            t = time.perf_counter()
            files, x_files = pre_scan_handler(_target=_target)
            print(f'[Files] {len(files)}')
            print(f'[Skipping Files] {len(x_files)}')
            if verbose is True:
                print(f'[Pre-Scan Time] {time.perf_counter() - t}')
            asyncio.run(async_write_scan_results(*files, file='pre_scan_files_'+dt+'.txt', _dt=dt))
            asyncio.run(async_write_scan_results(*x_files, file='pre_scan_x_files_'+dt+'.txt', _dt=dt))

            # chunk data ready for async multiprocess
            chunks = chunk_handler.chunk_data(files, _proc_max)
            if verbose is True:
                print('[Expected Number Of Chunks]', len(chunks))

            # prepare a dictionary of useful things for each child process
            multiproc_dict = {'files_recognized': recognized_files,
                              'buffer_max': _buffer_max,
                              'digits': _digits}

            # run the async multiprocess operation(s)
            print(f'[Scanning Target] ..')
            t = time.perf_counter()
            results = asyncio.run(main(chunks, multiproc_dict, mode))
            if verbose is True:
                print(f'[Chunks of Results] {len(results)}')
                print(f'[Async Multi-Process Time] {time.perf_counter()-t}')
            results = chunk_handler.un_chunk_data(results, depth=1)
            print(f'[Results] {len(results)}')
            # print('[Results]', results)

            # post scan: learn
            if mode == '--learn':
                print(f'[New Definitions] {len(results)}')
                if len(results) >= 1:
                    print('[Updating Definitions] ..')
                    asyncio.run(async_write_definitions(*results, file=_db_recognized_files))

            # post scan: deobfuscation
            elif mode == '--de-scan':
                print(f'[Unrecognized Files] {len(results)}')
                if len(results) >= 1:
                    print('[Writing Scan Results] ..')
                    asyncio.run(async_write_scan_results(*results, file='scan_results__'+dt+'.txt', _dt=dt))

            print('[Complete]')
            print('')

        else:
            # if os.path.exists(_target) and os.path.exists(_db_recognized_files):
            print('[Invalid Input]')
            if not os.path.exists(_target):
                print('[Invalid Target]', _target)
            if not os.path.exists(_db_recognized_files):
                print('[Invalid Database]', _db_recognized_files)
            omega_find_help.omega_help()
