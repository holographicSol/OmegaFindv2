""" Written by Benjamin Jack Cullen """
import os

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
    [fp.append(entry.path) for entry in scantree(path)]
    return [fp, x_files]


def search_scan(path: str, q: str) -> list:
    fp = []
    i_match = 0
    for entry in scantree(path):
        p = entry.path
        if q in p:
            print(f'[?][{i_match}] {p}')
            fp.append(p)
            i_match += 1
    return fp
