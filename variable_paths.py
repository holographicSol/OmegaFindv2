""" Written by Benjamin Jack Cullen """

import sys


def get_executable_path():
    if getattr(sys, 'frozen', False):
        _program_root = sys.executable
        idx = _program_root.rfind('\\')
        _program_root = _program_root[:idx]
    else:
        _program_root = '.\\'
    return _program_root


# program root
program_root = get_executable_path()

# database
database_dir = '\\db\\'
database_file = 'database_file_recognition.txt'
database_dir_path = program_root + database_dir
database_file_path = program_root + database_dir + database_file

# data
data_dir = '\\data\\'
data_dir_path = program_root + data_dir

# log
log_dir = '\\log\\'
log_dir_path = program_root + log_dir

# tmp
tmp_dir = '\\tmp\\'
tmp_dir_path = program_root + tmp_dir

# custom group csfx
csfx_dir = program_root
csfx_file = 'csfx_group.txt'
csfx_file_path = database_dir + csfx_file
