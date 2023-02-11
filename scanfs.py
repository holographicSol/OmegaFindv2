""" Written by Benjamin Jack Cullen """
import os
import time

import handler_print

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
            handler_print.display_search_scan_result(i_match, p)
            fp.append(p)
            i_match += 1
    handler_print.display_spacer()
    return fp


def pre_scan_handler(_target: str, _verbose: bool) -> tuple:
    t = time.perf_counter()
    scan_results = scan(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    completion_time = time.perf_counter()-t
    if _verbose is True:
        handler_print.display_prescan_info(_files, _x_files, completion_time)
    return _files, _x_files
