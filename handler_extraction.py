import os.path
import zipfile
import py7zr
import tarfile
import gzip


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


def incompatible_non_variant(_file: str, _buffer: str):
    split_buffer = _buffer.split(' ')
    if len(split_buffer) >= 2:
        if _buffer.split(' ')[1] in ['archive', 'compressed']:
            return ['[INCOMPATIBLE NON-VARIANT]', _file, _buffer]
