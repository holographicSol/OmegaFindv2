""" Written by Benjamin Jack Cullen """
import os
import time

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
    print('')
    return fp


def pre_scan_handler(_target: str) -> tuple:
    t = time.perf_counter()
    scan_results = scan(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    print(f'-- found {len(_files)} files during pre-scan (errors: {len(_x_files)}). time: {time.perf_counter()-t}')
    return _files, _x_files
