""" Written by Benjamin Jack Cullen """

import datetime
import os
import re
import codecs
import aiofiles
import asyncio
import magic
import pathlib
import shutil
import handler_print
import variable_paths
import variable_strings
import handler_strings
import tabulate
import cli_character_limits
import handler_post_process
import tabulate_helper

debug = False
result = []
program_root = variable_paths.program_root


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def ensure_db_file(fname: str):
    open(variable_paths.database_dir_path + fname, 'a+').close()


async def async_read_bytes(file: str, _buffer_max: int) -> bytes:
    async with aiofiles.open(file, mode='rb') as handle:
        _bytes = await handle.read(_buffer_max)
        await handle.close()
    return await asyncio.to_thread(file_sub_ops, _bytes)


async def read_file(file: str):
    data = []
    if os.path.exists(file):
        async with aiofiles.open(file, mode='r', encoding='utf8') as handle:
            data = await handle.read()
    return data


async def read_report(fname: str):
    _data = await read_file(file=fname)

    # get report subject column indexes
    _data_split = _data.split('\n')
    indexes = []
    for item in _data_split:
        if item.startswith('---'):
            item = item.split(' ')
            indexes = [len(item[0]), len(item[2]), len(item[4]), len(item[6])]
            break

    # parse report by indexes
    headers = []
    _results = []
    i_line = 0
    for item in _data_split:
        if i_line == 0:
            item_str = str(item)
            item_list = item_str.split('  ')
            no_empty_strings = [string for string in item_list if string != ""]
            headers = [no_empty_strings[0], no_empty_strings[1], no_empty_strings[2],
                       no_empty_strings[3] + '    ' + no_empty_strings[4]]
        if item is not None and i_line >= 2:
            item_str = str(item)
            try:
                mtime = item_str[:indexes[0]]
                buff = item_str[indexes[0]:indexes[0]+indexes[1]+2].strip()
                _bytes = item_str[indexes[0]+indexes[1]+2:indexes[0]+indexes[1]+indexes[2]+4].strip()
                filepath = item_str[indexes[0]+indexes[1]+indexes[2]+4:indexes[0]+indexes[1]+indexes[2]+indexes[3]+6].strip()
                _results.append([mtime, buff, _bytes, filepath])
            except:
                pass
        i_line += 1

    # enumeration for reasonable column widths
    max_column_width = cli_character_limits.column_width_from_tput(n=4)
    max_column_width_tot = max_column_width * 4
    max_dt = handler_post_process.longest_item(_results, idx=0)
    max_bytes = handler_post_process.longest_item(_results, idx=2)
    new_max_path = max_column_width_tot - max_dt - max_column_width - max_bytes - 4

    # create results table
    table_1 = tabulate.tabulate(_results,
                                colalign=('left', 'right', 'right', 'left'),
                                maxcolwidths=[max_dt, max_column_width, max_bytes, new_max_path],
                                stralign='left',
                                tablefmt='simple',
                                headers=(headers[0], headers[1], headers[2], headers[3]))
    # display results table
    print('')
    print('')
    print(f'[Scan Report] {fname}')
    print('')
    print('')
    tabulate_helper.display_rows_interactively(max_limit=75,
                                               results=_results,
                                               table=table_1,
                                               extra_input=False,
                                               message='\n-- more --\n',
                                               function=None)


async def read_definitions(fname: str) -> tuple:
    recognized_files, suffixes = [], []
    _data = await read_file(file=fname)
    _data = _data.split('\n')
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        buffer = datas[idx+1:]
        buffer = re.sub(variable_strings.digi_str, '', buffer)
        recognized_files.append([suffix, buffer])
        if suffix not in suffixes:
            suffixes.append(suffix)
    return recognized_files, suffixes


async def read_type_definitions(fname: str, _type_suffix: list) -> tuple:
    recognized_files, suffixes = [], []
    _data = await read_file(file=fname)
    _data = _data.split('\n')
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        if suffix in _type_suffix:
            buffer = datas[idx+1:]
            buffer = re.sub(variable_strings.digi_str, '', buffer)
            recognized_files.append([buffer])
            if suffix not in suffixes:
                suffixes.append(suffix)
    return recognized_files, suffixes


async def write_definitions(*args, file: str):
    if not os.path.exists(variable_paths.database_dir_path):
        os.mkdir(variable_paths.database_dir_path)
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg[0] + ' ' + arg[1]) for arg in args))
        await handle.write('\n')


async def write_scan_results(*args, file: str, _dt: str):
    target_dir = variable_paths.data_dir_path + _dt + '\\'
    if not os.path.exists(variable_paths.data_dir_path):
        os.mkdir(variable_paths.data_dir_path)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    file = target_dir + file
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg) for arg in args))
        await handle.write('\n')
        await handle.write('\n')


async def write_exception_log(*args, file: str, _dt: str):
    target_dir = variable_paths.log_dir_path + _dt + '\\'
    if not os.path.exists(variable_paths.log_dir_path):
        os.mkdir(variable_paths.log_dir_path)
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


def db_read_handler(_learn_bool: bool, _de_scan_bool: bool, _type_scan_bool: bool,
                    _db_recognized_files: str, _type_suffix: list) -> tuple:
    recognized_files, suffixes = [], []
    if _learn_bool is True or _de_scan_bool is True:
        recognized_files, suffixes = asyncio.run(read_definitions(fname=_db_recognized_files))
    elif _type_scan_bool is True:
        recognized_files, suffixes = asyncio.run(read_type_definitions(fname=_db_recognized_files,
                                                                       _type_suffix=_type_suffix))
    return recognized_files, suffixes


def read_bytes(file: str) -> bytes:
    with open(file, 'rb') as fo:
        _bytes = fo.read(2048)
    fo.close()
    return _bytes


def get_suffix(file: str) -> str:
    sfx = pathlib.Path(file).suffix
    sfx = sfx.replace('.', '').lower()
    if sfx == '':
        sfx = 'no_file_extension'
    return sfx


def get_m_time(file: str):
    dt = str(datetime.datetime.fromtimestamp(os.path.getmtime(file)))
    dt = dt.replace('-', ' ')
    dt = dt.split(' ')
    dt = dt[2] + '/' + dt[1] + '/' + dt[0] + '    ' + dt[3]
    if '.' in dt:
        dt = dt.split('.')
        dt = dt[0]
    return dt


def get_size(file: str) -> int:
    return os.path.getsize(file)


async def stat_files(_results, _target, _tmp):
    final_result = []
    for r in _results:
        if r[0] == '[ERROR]':
            if r not in final_result:
                final_result.append(r)
        else:
            regex_fname = str(r[1]).replace(_target, _tmp)
            if os.path.exists(r[1]):
                m = await asyncio.to_thread(get_m_time, r[1])
                s = await asyncio.to_thread(get_size, r[1])
                sub_result = [m, r[2], s, r[1]]
                if sub_result not in final_result:
                    final_result.append(sub_result)
            elif os.path.exists(regex_fname):
                m = await asyncio.to_thread(get_m_time, regex_fname)
                s = await asyncio.to_thread(get_size, regex_fname)
                sub_result = [m, r[2], s, r[1]]
                if sub_result not in final_result:
                    final_result.append(sub_result)
    return final_result


def file_sub_ops(_bytes: bytes) -> str:
    buff = ''
    try:
        buff = magic.from_buffer(_bytes)
    except Exception as e:
        if debug is True:
            handler_print.display_exception(_msg='-- exception:', e=e)
    return buff


def rem_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)


def call_input_open_dir(_results):
    if handler_strings.input_open_dir(_list=_results) is True:
        # got digit: ask again
        call_input_open_dir(_results)
