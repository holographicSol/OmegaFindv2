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
import prescan
import chunk_handler
import pathlib
import aiofiles
import omega_find_learn
import omega_find_deobfuscate


learn_seen_before = []


def pre_scan_handler(_target: str) -> list:
    scan_results = prescan.scan(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    return _files, _x_files


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


async def read_bytes(file: str) -> bytes:
    async with aiofiles.open(file, mode='rb') as handle:
        _bytes = await handle.read(1024)
        await handle.close()
    return await asyncio.to_thread(file_sub_ops, _bytes)


async def scan_learn_check(suffix: str, buffer: bytes, _recognized_files):
    if [suffix, buffer] not in _recognized_files:
        if [suffix, buffer] not in learn_seen_before:
            learn_seen_before.append([suffix, buffer])
            return [suffix, buffer]


async def scan_learn(file: str, _recognized_files: list) -> list:
    global learn_seen_before
    try:
        buffer = await read_bytes(file)
        suffix = await asyncio.to_thread(get_suffix, file)
        return await scan_learn_check(suffix, buffer, _recognized_files)
    except:
        pass


async def de_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files):
    if [suffix, buffer] not in _recognized_files:
        return [file, suffix, buffer]


async def de_scan(file: str, _recognized_files: list) -> list:
    global learn_seen_before
    try:
        buffer = await read_bytes(file)
        suffix = await asyncio.to_thread(get_suffix, file)
        return await de_scan_check(file, suffix, buffer, _recognized_files)
    except:
        pass


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.values()
    _recognized_files = chunk_handler.un_chunk_data(_recognized_files, depth=1)
    return [await scan_learn(item, _recognized_files) for item in chunk]


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.values()
    return [await de_scan(item, *_recognized_files) for item in chunk]


async def main(_chunks: list, _recognized_files: list, _mode: str):
    async with Pool() as pool:
        if mode == '--learn':
            _results = await pool.map(entry_point_learn, _chunks, {'my excellent foobar': _recognized_files})
        elif mode == '--de-scan':
            _results = await pool.map(entry_point_de_scan, _chunks, {'my excellent foobar': _recognized_files})
    return _results


async def async_read_definitions(fname):
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


def perform_checks(_mode: str, _target: str, _proc_max: int) -> bool:
    modes = ['--learn', '--de-scan']
    _allow_x = False
    if mode:
        if mode in modes:
            if _target:
                if os.path.exists(_target):
                    if _proc_max:
                        if str(_proc_max).isdigit():
                            _allow_x = True
    return _allow_x


if __name__ == '__main__':
    # Requires the aiomultiprocess pool file that I personally modified or this will not work.

    # WARNING: ensure sufficient ram/page-file/swap if changing read_bytes(bytes). ensure _proc_max suits your system.
    _db_recognized_files = './db/database_file_recognition.txt'
    # mode = '--de-scan'
    mode = '--de-scan'
    # _target = 'D:\\TEST\\'
    # _target = 'D:\\Music\\'
    _target = 'C:\\Windows\\'
    _proc_max = 32

    # mode = str(sys.argv[1])
    # _target = str(sys.argv[2])
    # _proc_max = int(sys.argv[3])

    # basic sys.argv checks
    allow_x = perform_checks(mode, _target, _proc_max)

    if allow_x is True:
        print('\n[OmegaFind v2]')
        # create datetime tag
        dt = str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')

        # read recognized files
        recognized_files, suffixes = [], []
        if os.path.exists(_db_recognized_files):
            recognized_files, suffixes = asyncio.run(async_read_definitions(fname=_db_recognized_files))
        else:
            open(_db_recognized_files, 'w').close()
        print(f'[Recognized Buffers] {len(recognized_files)}')
        print(f'[Known Suffixes] {len(suffixes)}')

        # pre-scan
        print('[Pre-Scanning]')
        t = time.perf_counter()
        files, x_files = pre_scan_handler(_target=_target)
        print(f'[Files] {len(files)}')
        print(f'[Skipping Files] {len(x_files)}')
        print(f'[Pre-Scan Time] {time.perf_counter() - t}')

        # log all paths
        asyncio.run(async_write_scan_results(*files, file='pre_scan_files_'+dt+'.txt', _dt=dt))

        # log paths that encountered an error
        asyncio.run(async_write_scan_results(*x_files, file='pre_scan_x_files_'+dt+'.txt', _dt=dt))

        # chunk data ready for async multiprocess
        chunks = chunk_handler.chunk_data(files, _proc_max)
        print('[Expected Number Of Chunks]', len(chunks))

        # run the async multiprocess operation(s)
        print(f'[Scanning Target]')
        t = time.perf_counter()
        results = asyncio.run(main(chunks, recognized_files, mode))
        print(f'[Chunks of Results] {len(results)}')
        print(f'[Async Multi-Process Time] {time.perf_counter()-t}')

        # un-chunk results
        results = chunk_handler.un_chunk_data(results, depth=1)
        print(f'[Results] {len(results)}')
        print('[Results]', results)

        if mode == '--learn':
            print(f'[New Definitions] {len(results)}')
            if len(results) >= 1:
                print('[Updating Definitions]')
                asyncio.run(async_write_definitions(*results, file=_db_recognized_files))

        elif mode == '--de-scan':
            print(f'[Unrecognized Files] {len(results)}')
            if len(results) >= 1:
                print('[Writing Scan Results]')
                asyncio.run(async_write_scan_results(*results, file='scan_results__'+dt+'.txt', _dt=dt))

        print('[Complete]')

    else:
        print('[invalid input]')
