""" Written by Benjamin Jack Cullen """

import datetime
import os
import time
import cli_character_limits
import handler_print
import tabulate
import tabulate_helper
import handler_file
import handler_post_process

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


def scan_depth_zero(path: str) -> list:
    global x_files
    path_list = os.listdir(path)
    file_list = []
    idx = 0
    for f in path_list:
        path_list[idx] = os.path.join(path, f)
        if os.path.isfile(path_list[idx]):
            file_list.append(path_list[idx])
        idx += 1
    return [file_list, []]


def search_scan(path: str, q: str, interact: bool, human_size=False) -> list:
    fp = []
    i_match = 0
    for entry in scantree(path):
        p = entry.path
        if q in p:
            if p not in fp:
                try:
                    sz = handler_file.get_size(p, human_size)
                    mt = handler_file.get_m_time(p)
                    fp.append([i_match, mt, sz, p])
                    i_match += 1
                except Exception as e:
                    fp.append([i_match, '[?]', '[?]', p, e])
                    i_match += 1
                    pass
    if fp:
        max_column_width = cli_character_limits.column_width_from_shutil(n=4, reduce=0)
        max_column_width_tot = max_column_width * 4
        max_index = handler_post_process.longest_item(fp, idx=0)+5
        max_dt = handler_post_process.longest_item(fp, idx=1)
        max_bytes = handler_post_process.longest_item(fp, idx=2)
        new_max_path = max_column_width_tot - max_index - max_dt - max_bytes - 4
        table_0 = tabulate.tabulate(fp,
                                    maxcolwidths=[max_index, max_dt, max_bytes, new_max_path],
                                    headers=(f'[Index]', '[Modified]', '[Bytes]', f'[Files: {len(fp)}]'),
                                    stralign='left')
        if interact is True:
            if len(fp) > 75:
                _message = '\n-- more or select --\n'
            else:
                _message = '\n-- select --\n'
            tabulate_helper.display_rows_interactively(max_limit=75,
                                                       results=fp,
                                                       table=table_0,
                                                       extra_input=True,
                                                       message=_message,
                                                       function=handler_file.call_input_open_dir)
        else:
            print(table_0)
    return fp


def pre_scan_handler(_target: str, _verbose: bool, _recursive: bool) -> tuple:
    t = time.perf_counter()
    if _recursive is True:
        scan_results = scan(path=_target)
    else:
        scan_results = scan_depth_zero(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    return _files, _x_files
