""" Written by Benjamin Jack Cullen """
import os
import re
import codecs
import aiofiles


async def read_definitions(fname: str) -> tuple:
    recognized_files, suffixes = [], []
    if os.path.exists(fname):
        digi_str = r'[0-9]'
        async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
            _data = await handle.read()
        _data = _data.split('\n')
        recognized_files = []
        _suffixes = []
        for datas in _data:
            idx = datas.find(' ')
            suffix = datas[:idx]
            buffer = datas[idx+1:]
            buffer = re.sub(digi_str, '', buffer)
            recognized_files.append([suffix, buffer])
            if suffix not in _suffixes:
                _suffixes.append(suffix)
    else:
        print(f'[Database] {fname} not found')
    print(f'[Recognized Buffers] {len(recognized_files)}')
    print(f'[Known Suffixes] {len(suffixes)}')
    return recognized_files, _suffixes


async def read_type_definitions(fname: str, _type_suffix: list) -> tuple:
    digi_str = r'[0-9]'
    async with aiofiles.open(fname, mode='r', encoding='utf8') as handle:
        _data = await handle.read()
    _data = _data.split('\n')
    _file_recognition_store = []
    _suffixes = []
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        if suffix in _type_suffix:
            buffer = datas[idx+1:]
            buffer = re.sub(digi_str, '', buffer)
            _file_recognition_store.append([buffer])
            if suffix not in _suffixes:
                _suffixes.append(suffix)
    return _file_recognition_store, _suffixes


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
    print(f'[Clean Database] {fname}')
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
    print('[Sorting] ..')
    db_store_new = sorted(clean_db_store)
    print(f'[Sorted {len(db_store_new)} items]')
    async with aiofiles.open(fname, mode='w', encoding='utf8') as handle:
        await handle.write('\n'.join(str(entry) for entry in db_store_new))
        await handle.write('\n')
    print(f'[Removed {str(_i_dups)} duplicates]')
    print(f'[Removed {str(_i_empty)} empty lines]')
    print('')
