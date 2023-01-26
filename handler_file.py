""" Written by Benjamin Jack Cullen """
import os
import re
import time
import codecs
import aiofiles
import scanfs


async def read_definitions(fname: str) -> tuple:
    recognized_files, suffixes = [], []
    if os.path.exists(fname):
        digi_str = r'[0-9]'
        async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
            _data = await handle.read()
        _data = _data.split('\n')
        recognized_files = []
        suffixes = []
        for datas in _data:
            idx = datas.find(' ')
            suffix = datas[:idx]
            buffer = datas[idx+1:]
            buffer = re.sub(digi_str, '', buffer)
            recognized_files.append([suffix, buffer])
            if suffix not in suffixes:
                suffixes.append(suffix)
    return recognized_files, suffixes


async def read_type_definitions(fname: str, _type_suffix: list) -> tuple:
    recognized_files, suffixes = [], []
    if os.path.exists(fname):
        digi_str = r'[0-9]'
        async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
            _data = await handle.read()
        _data = _data.split('\n')
        recognized_files = []
        suffixes = []
        for datas in _data:
            idx = datas.find(' ')
            suffix = datas[:idx]
            if suffix in _type_suffix:
                buffer = datas[idx+1:]
                buffer = re.sub(digi_str, '', buffer)
                recognized_files.append([buffer])
                if suffix not in suffixes:
                    suffixes.append(suffix)
    return recognized_files, suffixes


async def write_definitions(*args, file: str):
    if not os.path.exists('./db/'):
        os.mkdir('./db/')
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg[0] + ' ' + arg[1]) for arg in args))
        await handle.write('\n')


async def write_scan_results(*args, file: str, _dt: str):
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


async def write_exception_log(*args, file: str, _dt: str):
    target_dir = './log/' + _dt + '/'
    if not os.path.exists('./log/'):
        os.mkdir('./log/')
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    file = target_dir + file
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg) for arg in args))


async def clean_database(fname: str):
    async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
        _data = await handle.read()
    _data = _data.split('\n')
    clean_db_store = []
    _i_dups = 0
    _i_empty = 0
    for datas in _data:
        if datas != '':
            if datas not in clean_db_store:
                clean_db_store.append(datas)
            else:
                _i_dups += 1
        else:
            _i_empty += 1
    db_store_new = sorted(clean_db_store)
    async with aiofiles.open(fname, mode='w', encoding='utf8') as handle:
        await handle.write('\n'.join(str(entry) for entry in db_store_new))
        await handle.write('\n')


def pre_scan_handler(_target: str) -> tuple:
    print('[Pre-Scanning] ..')
    t = time.perf_counter()
    scan_results = scanfs.scan(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    print(f'[Files] {len(_files)}')
    print(f'[Errors] {len(_x_files)}')
    print(f'[Pre-Scan Time] {time.perf_counter() - t}')
    return _files, _x_files
