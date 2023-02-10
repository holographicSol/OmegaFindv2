""" Written by Benjamin Jack Cullen """
import os
import sys
import re
import codecs
import aiofiles
import asyncio
import patoolib
import handler_extraction_method
import magic
import pathlib
import shutil
import variables_compat_archives

debug = False
result = []


def get_executable_path():
    if getattr(sys, 'frozen', False):
        _program_root = sys.executable
        idx = _program_root.rfind('\\')
        _program_root = _program_root[:idx]
    else:
        _program_root = '.\\'
    return _program_root


program_root = get_executable_path()


def ensure_db():
    if not os.path.exists(program_root+'\\db\\'):
        os.mkdir(program_root+'\\db\\')
    if not os.path.exists(program_root+'\\db\\database_file_recognition.txt'):
        open(program_root+'\\db\\database_file_recognition.txt', 'w').close()


async def async_read_bytes(file: str, _buffer_max: int) -> bytes:
    async with aiofiles.open(file, mode='rb') as handle:
        _bytes = await handle.read(_buffer_max)
        await handle.close()
    return await asyncio.to_thread(file_sub_ops, _bytes)


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
    if not os.path.exists(program_root+'\\db\\'):
        os.mkdir(program_root+'\\db\\')
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg[0] + ' ' + arg[1]) for arg in args))
        await handle.write('\n')


async def write_scan_results(*args, file: str, _dt: str):
    target_dir = program_root+'\\data\\' + _dt + '\\'
    if not os.path.exists(program_root+'\\data\\'):
        os.mkdir(program_root+'\\data\\')
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    file = target_dir + file
    if not os.path.exists(file):
        codecs.open(file, "w", encoding='utf8').close()
    async with aiofiles.open(file, mode='a', encoding='utf8') as handle:
        await handle.write('\n'.join(str(arg) for arg in args))


async def write_exception_log(*args, file: str, _dt: str):
    target_dir = program_root+'\\log\\' + _dt + '\\'
    if not os.path.exists(program_root+'\\log\\'):
        os.mkdir(program_root+'\\log\\')
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


def extract_exception_handler(file: str, _static_tmp: str, _target: str, buffer: str, e: Exception, msg: str):
    # print(f'[E] [{file} {buffer}] {e}')
    _result = []
    if 'Password is required' in str(e):
        fullpath = file.replace(_static_tmp, _target)
        _result = ['Password required', str(fullpath), buffer]
        if _result not in result:
            return _result
    else:
        fullpath = file.replace(_static_tmp, _target)
        _result = [msg, str(fullpath), str(buffer), str(e)]
        if _result not in result:
            return _result


def extract_nested_compressed(file: str, temp_directory: str, _target: str, _static_tmp: str) -> tuple:
    result_bool = False
    global result
    buffer = ''
    try:
        # read file with magic
        buffer = file_sub_ops(read_bytes(file=file))
        buffer = str(buffer).strip()
        try:
            # +/- compatibility

            # method: zipfile module
            if buffer.startswith(tuple(variables_compat_archives.group_zipfile_compat)):
                handler_extraction_method.ex_zip(_file=file, _temp_directory=temp_directory)

            # method: py7zr module
            elif buffer.startswith(tuple(variables_compat_archives.group_py7zr_compat)):
                handler_extraction_method.ex_py7zr(_file=file, _temp_directory=temp_directory)

            # method 0: tarfile module
            elif buffer.startswith(tuple(variables_compat_archives.group_tarfile_compat)):
                try:
                    handler_extraction_method.ex_tarfile(_file=file, _temp_directory=temp_directory)
                except:
                    # method 1: gzip module
                    handler_extraction_method.ex_gzip(_file=file, _temp_directory=temp_directory)

        except Exception as e:
            if 'Password' in str(e):
                result.append(extract_exception_handler(file=file, _static_tmp=_static_tmp, _target=_target,
                                                        buffer=buffer, e=e, msg=''))
            else:
                # method: patool
                try:
                    split_buff = buffer.split(' ')
                    if len(split_buff) >= 2:
                        if split_buff[1] in ['compressed', 'archive']:
                            patoolib.extract_archive(archive=file, outdir=temp_directory, verbosity=0)
                except Exception as e:
                    # log incompatible
                    non_variant = handler_extraction_method.incompatible_non_variant(_file=file, _buffer=buffer, e=e)
                    if non_variant:
                        result.append(non_variant)

        # attempt to walk in extracted contents
        if os.path.exists(temp_directory):
            result_bool = True
            for root, dirs, files in os.walk(temp_directory):
                for filename in files:

                    # check if file looks like a compatible archive
                    buffer = file_sub_ops(read_bytes(file=file))
                    buffer = str(buffer).strip()

                    split_buff = buffer.split(' ')
                    if len(split_buff) >= 2:
                        if split_buff[1] in ['compressed', 'archive']:

                            # re-iterate
                            fileSpec = os.path.join(root, filename)
                            extract_nested_compressed(file=fileSpec,
                                                      temp_directory=fileSpec.replace(pathlib.Path(filename).suffix, ''),
                                                      _target=_target,
                                                      _static_tmp=_static_tmp)

    except Exception as e:
        result.append(extract_exception_handler(file=file, _static_tmp=_static_tmp, _target=_target, buffer=buffer, e=e,
                                                msg='[ERROR]'))
    return result_bool, result


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


def file_sub_ops(_bytes: bytes) -> str:
    buff = ''
    try:
        buff = magic.from_buffer(_bytes)
    except Exception as e:
        if debug is True:
            print(f'-- exception: {e}')
    return buff


def rem_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
