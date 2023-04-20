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
import PyPDF2
import ebooklib
from ebooklib import epub
import subprocess
import handler_file

info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0
main_pid = int()

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


async def read_file(file: str) -> list:
    data = []
    if os.path.exists(file):
        async with aiofiles.open(file, mode='r', encoding='utf8') as handle:
            data = await handle.read()
    return data


async def async_read_all_bytes(file: str) -> list:
    data = []
    if os.path.exists(file):
        async with aiofiles.open(file, mode='rb') as handle:
            data = await handle.read()
    return data


def pytopdf_read(pdf_file: str):
    return PyPDF2.PdfReader(pdf_file, strict=False)


def pytopdf_get_pages(pdf_reader) -> int:
    return len(pdf_reader.pages)


def pytoodf_extract(page_num: int, _search_str: str, pdf_reader):
    page_text = pdf_reader.pages[page_num].extract_text()
    return page_text


def string_match(_search_str: str, _text: str):
    if handler_strings.canonical_caseless(_search_str) in handler_strings.canonical_caseless(_text):
        return True


def read_all_bytes(file_in: str):
    return open(file_in, 'rb')


async def str_in_pdf(file_in='', _search_str=''):
    """ look for search_str in file """
    try:
        pdf_file = await asyncio.to_thread(read_all_bytes, file_in=file_in)
        pdf_reader = await asyncio.to_thread(pytopdf_read, pdf_file=pdf_file)
        n_pages = await asyncio.to_thread(pytopdf_get_pages, pdf_reader=pdf_reader)
        for page_num in range(n_pages):
            _text = await asyncio.to_thread(pytoodf_extract,
                                            page_num=page_num, pdf_reader=pdf_reader, _search_str=_search_str)
            _text = str(_text).strip()
            _result = await asyncio.to_thread(string_match, _search_str=_search_str, _text=_text)
            if _result is True:
                pdf_file.close()
                return file_in
        pdf_file.close()
    except Exception as e:
        print(f'{e} {file_in}')
        return ['[ERROR] ', str(e), str(file_in)]


async def str_in_epub(file_in='', _search_str=''):

    book = epub.read_epub(file_in)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content()
            if handler_strings.canonical_caseless(_search_str) in handler_strings.canonical_caseless(str(content)).strip():
                return file_in


async def str_in_txt(file_in='', _search_str=''):
    with codecs.open(file_in, 'r', encoding='utf8') as fo:
        for line in fo:
            line = line.strip()
            if string_match(_search_str=_search_str, _text=line) is True:
                return file_in


def convert_all_to_text(file_in='', _program_root='', _verbose=False):
    _tmp_dir = _program_root + '\\tmp\\' + str(handler_strings.randStr()) + '\\'
    filename_idx = file_in.rfind('\\')
    filename = file_in[filename_idx:]
    _tmp = _tmp_dir + filename+'.txt'

    cmd = '"./python.exe" ./unoconv/unoconv -o "' + _tmp + '" -f txt "' + file_in + '"'
    if _verbose is True:
        print(f'-- running command: {cmd}')
    xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info)
    while True:
        output = xcmd.stdout.readline()
        if output == '' and xcmd.poll() is not None:
            break
        if output and _verbose is True:
            output_str = str(output.decode("utf-8").strip())
            print(output_str)
        else:
            break
    rc = xcmd.poll()
    if os.path.exists(_tmp):
        return _tmp, _tmp_dir


async def file_reader(file: str, _query: str, _verbose: bool, _buffer: str, _program_root: str) -> list:
    """ todo -->
    Intention: File reader method filter for string matching.
               Methods should be filtered by buffer not a fname suffix (for power).
    * add further compatibility:
        1. anything incompatible with unoconv.
        2. anything that although compatible with unoconv that would also be faster to not convert to .txt.
    """

    if _verbose is True:
        print(f'scanning: {file}')

    if 'ASCII text' in _buffer:
        _result = await str_in_txt(file_in=file, _search_str=_query)
        if _result:
            return [_result]

    elif 'PDF' in _buffer:
        _result = await str_in_pdf(file_in=file, _search_str=_query)
        if _result:
            return [_result]

    elif 'EPUB' in _buffer:
        _result = await str_in_epub(file_in=file, _search_str=_query)
        if _result:
            return [_result]

    else:
        _tmp_file, _tmp_dir = await asyncio.to_thread(convert_all_to_text, file_in=file, _program_root=_program_root,
                                                      _verbose=_verbose)
        if _tmp_file:
            if _verbose is True:
                print(f'-- attempting to read: {_tmp_file}')
            _result = await str_in_txt(file_in=_tmp_file, _search_str=_query)
            if os.path.exists(_tmp_dir):
                handler_file.rem_dir(path=_tmp_dir)
            _result[1] = file
            if _result:
                return [_result]


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
    max_column_width = cli_character_limits.column_width_from_shutil(n=4)
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
        call_input_open_dir(_results)
