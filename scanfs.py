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
        x_files.append(['[ERROR]', str(e)])


def scan(path: str) -> list:
    global x_files
    x_files = []
    fp = []
    for entry in scantree(path):
        # print(f'entry: {entry}')
        # if entry.is_file():
        fp.append(entry.path)
    # [fp.append(entry.path) for entry in scantree(path) if entry.is_file()]
    return [fp, x_files]


def search_scan(path: str, q: str) -> list:
    fp = []
    i_match = 0
    for entry in scantree(path):
        print(f'entry: {entry}')
        if entry.is_file():
            if q in entry.path:
                print(f'[?][{i_match}] {entry.path}')
                fp.append(entry.path)
                i_match += 1
    return fp
