""" Written by Benjamin Jack Cullen """
import os
import handler_exception

x_files = []


def scantree(path: str) -> str:
    global x_files
    try:
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry
    except Exception as e:
        x_files.append(handler_exception.exception_format(e))


def scan(path: str) -> tuple:
    global x_files
    x_files = []
    fp = []
    [fp.append(entry.path) for entry in scantree(path) if entry.is_file()]
    return fp, x_files
