import sys


def get_path():
    if getattr(sys, 'frozen', False):
        program_root = sys.executable
        idx = program_root.rfind('\\')
        program_root = program_root[:idx]
    else:
        program_root = '.\\'
    return program_root
