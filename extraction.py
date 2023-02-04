import os
import time

import magic
import compatible_archives
import zipfile
import tarfile
import py7zr
import shutil
import gzip

debug = False


def file_sub_ops(_bytes: bytes) -> str:
    buff = ''
    try:
        buff = magic.from_buffer(_bytes)
    except Exception as e:
        if debug is True:
            print(f'-- exception: {e}')
    return buff


def read_bytes(file: str) -> bytes:
    with open(file, 'rb') as fo:
        _bytes = fo.read(2048)
    fo.close()
    return _bytes


for dirName, subdir, filelist in os.walk('D:\\TEST\\compatibility'):
    for fname in filelist:
        print('_'*21)
        file = os.path.join(dirName, fname)
        print('[FILE]', file)
        buffer = file_sub_ops(read_bytes(file=file))
        buffer = str(buffer).strip()

        # +/- compatibility
        try:
            print('[TESTING] zipfile')
            with zipfile.ZipFile(file, 'r') as extract_file:
                extract_file.extractall(path='./tmp/')
            print('[PASSED]', file, buffer, e)
        except Exception as e:
            print('[FAILED]', file, buffer, e)


        try:
            print('[TESTING] py7zr')
            with py7zr.SevenZipFile(file, 'r') as extract_file:
                extract_file.extractall(path='./tmp/')
            print('[PASSED]', file, buffer, e)
        except Exception as e:
            print('[FAILED]', file, buffer, e)

        try:
            print('[TESTING] tarfile')
            with tarfile.open(file, 'r') as extract_file:
                extract_file.extractall(path='./tmp/')
        except Exception as e:
            print('[FAILED]', file, buffer, e)

        try:
            print('[TESTING] gzip+shutil')
            GZ = gzip.GzipFile(file)
            contents = GZ.read()
            print(f"{file} is a gzip file with length: {len(contents)}")
            with open('./ungzipped.zip', 'wb') as new_file:
                new_file.write(contents)
            buffer = file_sub_ops(read_bytes(file='./ungzipped.zip'))
            buffer = str(buffer).strip()
            shutil.unpack_archive('./ungzipped.zip')
        except Exception as e:
            print('[FAILED]', file, buffer, e)
