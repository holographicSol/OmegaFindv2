""" Written by Benjamin Jack Cullen """

import datetime
import os
import time
import cli_character_limits
import handler_print
import tabulate
import handler_table_rows

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


def search_scan(path: str, q: str, interact: bool) -> list:
    fp = []
    i_match = 0
    for entry in scantree(path):
        p = entry.path
        if q in p:
            if p not in fp:
                try:
                    sz = os.path.getsize(p)
                    mt = os.path.getmtime(p)
                    mt = datetime.datetime.fromtimestamp(mt)
                    fp.append([i_match, mt, sz, p])
                    i_match += 1
                except Exception as e:
                    fp.append([i_match, '[?]', '[?]', p, e])
                    i_match += 1
                    pass
    if fp:
        max_column_width = cli_character_limits.column_width_from_screen_size_using_ratio(n=2, reduce=0, add=56)
        table_0 = tabulate.tabulate(fp,
                                    maxcolwidths=[max_column_width, max_column_width, max_column_width, max_column_width],
                                    headers=(f'Index', 'Modified', 'Bytes', 'Files'),
                                    stralign='left')
        if interact is True:
            handler_table_rows.display_rows_interactively(max_limit=75, _results=fp, table=table_0, open_dir=True)
        else:
            print(table_0)
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
    return _files, _x_files, completion_time
