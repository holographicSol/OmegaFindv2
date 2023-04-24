""" Written by Benjamin Jack Cullen """

import datetime
import os
import codecs
import time

import aiofiles
import asyncio
import magic
import pathlib
import shutil

import handler_input
import handler_print
import variable_paths
import handler_strings
import tabulate
import cli_character_limits
import handler_post_process
import PyPDF2
import ebooklib
from ebooklib import epub
import subprocess
import handler_file
import tabulate_helper2
import handler_chunk
import handler_input

info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0
main_pid = int()

debug = False
result = []
program_root = variable_paths.program_root
retry_limit_convert_all_to_text = 3


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def ensure_db_file(fname: str):
    open(variable_paths.database_dir_path + fname, 'a+').close()


async def async_read_bytes(_file: str, _buffer_max: int) -> bytes:
    async with aiofiles.open(_file, mode='rb') as handle:
        _bytes = await handle.read(_buffer_max)
        await handle.close()
    return await asyncio.to_thread(file_sub_ops, _bytes)


async def read_file(file: str) -> list:
    data = []
    if os.path.exists(file):
        async with aiofiles.open(file, mode='r', encoding='utf8') as handle:
            data = await handle.read()
        await handle.close()
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
        # print(f'{e} {file_in}')
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
    global retry_limit_convert_all_to_text

    _tmp_dir = _program_root + '\\tmp\\' + str(handler_strings.randStr()) + '\\'
    filename_idx = file_in.rfind('\\')
    filename = file_in[filename_idx:]
    _tmp = _tmp_dir + filename+'.txt'

    cmd = '"./python.exe" "./unoconv/unoconv" -o "' + _tmp + '" -f txt "' + file_in + '"'
    if _verbose is True:
        print(f'-- running command: {cmd}')
    xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info)
    try_again = False
    while True:
        output = xcmd.stdout.readline()
        if output == '' and xcmd.poll() is not None:
            break
        if output:
            output_str = str(output.decode("utf-8").strip())
            if _verbose is True:
                print(output_str)
            if 'Error' in output_str or 'Exception' in output_str or 'UnoException' in output_str or \
                    'untimeException' in output_str:
                try_again = True
                break
        else:
            break
    rc = xcmd.poll()
    if try_again is True:
        if retry_limit_convert_all_to_text > int(0):
            retry_limit_convert_all_to_text -= 1
            time.sleep(1)
            convert_all_to_text(file_in=file_in, _program_root=_program_root, _verbose=_verbose)
    retry_limit_convert_all_to_text = 3
    if os.path.exists(_tmp):
        return _tmp, _tmp_dir


async def file_reader(file: str, _query: str, _verbose: bool, _buffer: str, _program_root: str, _bench: bool) -> list:
    """ todo -->
    Intention: Filter different types of files into different read functions and then parse the file contents
               for _query.
    Adding compatibility:
        Try do do as much in memory as possible.
        Try to avoid defaulting to unoconv (to avoid touching disk and for speed/efficiency).
        Develop both standard_read_filters and unoconv_read_filters by analyzing files extensively (time consuming).
        Performance can greatly improve by developing standard_read_filters and unoconv_read_filters and by adding
        more compatibility before resorting to unoconv.
    """

    # Buffers for standard read filter (this filter is incomplete).
    standard_read_filters = ['ASCII text',
                             'XML',
                             'Rich Text Format',
                             'UTF-8 Unicode']

    # Buffers for unoconv filter  # uncomment to use this filter (this filter is incomplete).
    unoconv_read_filters = ['Composite Document File V2 Document',
                            'OpenDocument Text',
                            'OpenDocument Text Template',
                            'Zip archive data']

    if _verbose is True:
        print(f'scanning: {file}')

    read_mode = int(0)

    if _bench is True:
        t0 = time.perf_counter()

    # PDF: Specific PDF method
    if read_mode is int(0):
        if 'PDF' in _buffer:
            if _verbose is True:
                print(f'-- using pdf-method: {file}')
            read_mode = int(1)
            _result = await str_in_pdf(file_in=file, _search_str=_query)
            if _bench is True:
                print(f'pdf time ({file}): {time.perf_counter()-t0}')
            if _result:
                return [_result]

    # EPUB Specific EPUB method
    if read_mode is int(0):
        if 'EPUB' in _buffer:
            if _verbose is True:
                print(f'-- using epub-method: {file}')
            read_mode = int(1)
            _result = await str_in_epub(file_in=file, _search_str=_query)
            if _bench is True:
                print(f'epub filter time ({file}): {time.perf_counter()-t0}')
            if _result:
                return [_result]

    # Standard Filter (Text) Examples: txt, html, xml, sh, py, etc.
    # This method covers a lot of different file types both executable and non-executable.
    if read_mode is int(0):
        for standard_read_filter in standard_read_filters:
            if standard_read_filter in _buffer:
                if _verbose is True:
                    print(f'-- using standard-method: {file}')
                read_mode = int(1)
                _result = await str_in_txt(file_in=file, _search_str=_query)
                if _bench is True:
                    print(f'standard filter time ({file}): {time.perf_counter() - t0}')
                if _result:
                    return [_result]

    if read_mode is int(0):
        import handler_extraction_method
        _tmp = _program_root + '\\tmp\\' + str(handler_strings.randStr())
        handler_extraction_method.ex_zip(_file=file, _temp_directory=_tmp)
        if os.path.exists(_tmp):
            for d, s, fl in os.walk(_tmp):
                for f in fl:
                    print(f'-- extracted file: {f}')
                    fp = os.path.join(d, f)
                    read_mode = int(1)
                    _result = await str_in_txt(file_in=fp, _search_str=_query)
                    if _bench is True:
                        print(f'extract file filter time ({file}): {time.perf_counter() - t0}')
                    if _result:
                        return [file]

    # Unoconv Filter (Documents) Examples: docx, otg, ott, odt, odd, etc.
    if read_mode is int(0):
        for unoconv_read_filter in unoconv_read_filters:
            if unoconv_read_filter in _buffer:
                if _verbose is True:
                    print(f'-- using unoconv-method: {file}')
                _tmp_file, _tmp_dir = await asyncio.to_thread(convert_all_to_text, file_in=file, _program_root=_program_root,
                                                              _verbose=_verbose)
                if _tmp_file:
                    read_mode = int(1)
                    _result = await str_in_txt(file_in=_tmp_file, _search_str=_query)
                    if os.path.exists(_tmp_dir):
                        handler_file.rem_dir(path=_tmp_dir)

                    if _result:
                        _result = file
                        if _bench is True:
                            print(f'unoconv filter time ({file}): {time.perf_counter() - t0}')
                        return [_result]
                    break

    if read_mode is int(0):
        if _verbose is True:
            print(f'-- add compatibility for: {file} ({_buffer})')


async def read_report(fname: str):
    _data = await read_file(file=fname)

    # get report subject column indexes
    _data_split = str(_data).split('\n')
    indexes = []
    for item in _data_split:
        item = str(item).strip()
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
            headers = [no_empty_strings[0], no_empty_strings[1], no_empty_strings[2], no_empty_strings[3] + '    ' + no_empty_strings[4]]
        if item is not None and i_line >= 2:
            item_str = str(item)
            try:
                mtime = item_str[:indexes[0]]
                buff = item_str[indexes[0]:indexes[0]+indexes[1]+2].strip()
                _bytes = item_str[indexes[0]+indexes[1]+2:indexes[0]+indexes[1]+indexes[2]+4].strip()
                filepath = item_str[indexes[0]+indexes[1]+indexes[2]+4:indexes[0]+indexes[1]+indexes[2]+indexes[3]+6].strip()
                _results.append([mtime, buff, _bytes, filepath])
            except Exception as e:
                print(e)
        i_line += 1

    if len(indexes) == 4:
        # todo: pass all table headers through tabulate helper pad/newline function!
        chunk_size = 75
        tabulate.PRESERVE_WHITESPACE = True
        max_column_width = cli_character_limits.column_width_from_shutil(n=4)

        _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                         col_idx=2,
                                                                         max_column_width=None)
        _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                         col_idx=1,
                                                                         max_column_width=max_column_width)
        max_column_width_tot = max_column_width * 4
        max_dt = handler_post_process.longest_item(_results, idx=0)
        max_bytes = handler_post_process.longest_item(_results, idx=2)
        new_max_path = max_column_width_tot - max_dt - max_column_width - max_bytes - 8
        _results = handler_chunk.chunk_data(data=_results, chunk_size=chunk_size)
        n_table = 0
        for _result in _results:
            try:
                if n_table == 0:
                    table_1 = tabulate.tabulate(_result,
                                                colalign=('left', 'right', 'right', 'left'),
                                                maxcolwidths=[max_dt, None, max_bytes, new_max_path],
                                                headers=(headers[0], headers[1], headers[2], headers[3]),
                                                stralign='left',
                                                floatfmt='f')
                else:
                    table_1 = tabulate.tabulate(_result,
                                                colalign=('left', 'right', 'right', 'left'),
                                                maxcolwidths=[max_dt, None, max_bytes, new_max_path],
                                                stralign='left',
                                                tablefmt='plain',
                                                floatfmt='f')
                print(table_1)
                n_table += 1
                if not _result == _results[-1]:
                    try:
                        handler_input.input_singularity(message='')
                    except KeyboardInterrupt:
                        print('logging: keyboard interrupt')
                        break
                    except:
                        pass
            except KeyboardInterrupt:
                print('logging: keyboard interrupt')
                break


async def read_definitions(fname: str, _digits=True) -> tuple:
    recognized_files, suffixes = [], []
    _data = await read_file(file=fname)
    _data = _data.split('\n')
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        buffer = datas[idx+1:]
        if _digits is False:
            buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=buffer)  # digitless
        recognized_files.append([suffix, buffer])
        if suffix not in suffixes:
            suffixes.append(suffix)
    return recognized_files, suffixes


async def read_type_definitions(fname: str, _type_suffix: list, _digits=True) -> tuple:
    recognized_files, suffixes = [], []
    _data = await read_file(file=fname)
    _data = _data.split('\n')
    for datas in _data:
        idx = datas.find(' ')
        suffix = datas[:idx]
        if suffix in _type_suffix:
            buffer = datas[idx+1:]
            if _digits is False:
                buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=buffer)  # digitless
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
                    _db_recognized_files: str, _type_suffix: list, _digits=True) -> tuple:
    recognized_files, suffixes = [], []
    if _learn_bool is True or _de_scan_bool is True:
        recognized_files, suffixes = asyncio.run(read_definitions(fname=_db_recognized_files, _digits=_digits))
    elif _type_scan_bool is True:
        recognized_files, suffixes = asyncio.run(read_type_definitions(fname=_db_recognized_files,
                                                                       _type_suffix=_type_suffix,
                                                                       _digits=_digits))
    return recognized_files, suffixes


def read_bytes(file: str) -> bytes:
    with open(file, 'rb') as fo:
        _bytes = fo.read(2048)
    fo.close()
    return _bytes


def get_suffix(_file: str) -> str:
    sfx = pathlib.Path(_file).suffix
    sfx = sfx.replace('.', '').lower()
    if sfx == '':
        sfx = 'no_file_extension'
    return sfx


def convert_timestamp_to_datetime(timestamp):
    dt = str(datetime.datetime.fromtimestamp(timestamp))
    dt = dt.replace('-', ' ')
    dt = dt.split(' ')
    dt = dt[2] + '/' + dt[1] + '/' + dt[0] + '    ' + dt[3]
    if '.' in dt:
        dt = dt.split('.')
        dt = dt[0]
    return dt


def get_m_time(_file: str):
    return str(os.path.getmtime(_file))


def get_size(_file: str) -> str:
    return str(os.path.getsize(_file))


async def stat_files(_results, _target, _tmp, _human_size=False):
    final_result = []
    for r in _results:
        if r[0] == '[ERROR]':
            if r not in final_result:
                final_result.append(r)
        else:
            regex_fname = str(r[1]).replace(_target, _tmp)
            if os.path.exists(r[1]):
                m = await asyncio.to_thread(get_m_time, _file=r[1])
                s = await asyncio.to_thread(get_size, _file=r[1])
                sub_result = [m, r[2], s, r[1]]
                if sub_result not in final_result:
                    final_result.append(sub_result)
            elif os.path.exists(regex_fname):
                m = await asyncio.to_thread(get_m_time, _file=regex_fname)
                s = await asyncio.to_thread(get_size, _file=regex_fname)
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
