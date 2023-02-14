""" Written by Benjamin Jack Cullen """

import os.path
import pathlib
import zipfile
import py7zr
import tarfile
import gzip
import patoolib
import handler_file
import variables_compat_archives

result = []


def ex_zip(_file: str, _temp_directory: str) -> None:
    with zipfile.ZipFile(_file, 'r') as extract_file:
        extract_file.extractall(path=_temp_directory + '\\')


def ex_py7zr(_file: str, _temp_directory: str) -> None:
    with py7zr.SevenZipFile(_file, 'r') as extract_file:
        extract_file.extractall(path=_temp_directory + '\\')


def ex_tarfile(_file: str, _temp_directory: str) -> None:
    with tarfile.open(_file, 'r') as extract_file:
        extract_file.extractall(path=_temp_directory + '\\')


def ex_gzip(_file: str, _temp_directory: str) -> None:
    GZ = gzip.GzipFile(_file)
    contents = GZ.read()
    idx = _file.rfind('\\')
    new_fname = _temp_directory + _file[idx:]
    if not os.path.exists(_temp_directory):
        os.makedirs(_temp_directory)
    with open(new_fname, 'wb') as new_file:
        new_file.write(contents)


def incompatible_non_variant(_file: str, _buffer: str, e: Exception):
    split_buffer = _buffer.split(' ')
    if len(split_buffer) >= 2:
        if _buffer.split(' ')[1] in ['archive', 'compressed']:
            return ['[INCOMPATIBLE NON-VARIANT]', str(_file), str(_buffer), str(e)]


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
        buffer = handler_file.file_sub_ops(handler_file.read_bytes(file=file))
        buffer = str(buffer).strip()

        try:
            # +/- compatibility

            # method: zipfile module
            if buffer.startswith(tuple(variables_compat_archives.group_zipfile_compat)):
                ex_zip(_file=file, _temp_directory=temp_directory)

            # method: py7zr module
            elif buffer.startswith(tuple(variables_compat_archives.group_py7zr_compat)):
                ex_py7zr(_file=file, _temp_directory=temp_directory)

            # method 0: tarfile module
            elif buffer.startswith(tuple(variables_compat_archives.group_tarfile_compat)):
                try:
                    ex_tarfile(_file=file, _temp_directory=temp_directory)
                except:
                    # method 1: gzip module
                    ex_gzip(_file=file, _temp_directory=temp_directory)

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
                            patoolib.extract_archive(archive=file, outdir=temp_directory)
                except Exception as e:
                    # log incompatible
                    non_variant = incompatible_non_variant(_file=file, _buffer=buffer, e=e)
                    if non_variant:
                        result.append(non_variant)

        # attempt to walk in extracted contents
        if os.path.exists(temp_directory):
            result_bool = True
            for root, dirs, files in os.walk(temp_directory):
                for filename in files:

                    # check if file looks like a compatible archive
                    buffer = handler_file.file_sub_ops(handler_file.read_bytes(file=file))
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
