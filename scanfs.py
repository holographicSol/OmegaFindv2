""" Written by Benjamin Jack Cullen """

import os
import time
import cli_character_limits
import tabulate
import handler_file
import handler_post_process
import handler_sort
import handler_convert_results
import tabulate_helper2
import handler_chunk

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


def search_scan(path: str, q: str, interact: bool, _sort_mode: str, human_size=False):
    fp = []
    for entry in scantree(path):
        p = entry.path
        if q in p:
            if p not in fp:
                try:
                    sz = handler_file.get_size(_file=p)
                    mt = handler_file.get_m_time(_file=p)
                    fp.append([mt, sz, p])
                except Exception as e:
                    fp.append(['[?]', '[?]', p, e])
                    pass
    if fp:
        fp = handler_sort.sort_len_2(data=fp, sort_mode=_sort_mode)
        _results = handler_convert_results.convert_string_match_results(fp, _human_size=human_size)

        chunk_size = 75
        tabulate.PRESERVE_WHITESPACE = True

        max_column_width = cli_character_limits.column_width_from_shutil(n=3)
        _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                         col_idx=1,
                                                                         max_column_width=None)
        # enumerate remaining column widths
        max_column_width_tot = max_column_width * 3
        max_dt = handler_post_process.longest_item(_results, idx=0)
        max_bytes = handler_post_process.longest_item(_results, idx=1)
        new_max_path = max_column_width_tot - max_dt - max_bytes - 8
        # chunk results by a reasonable number so as not to flood the console and loose results (interactive)
        _results = handler_chunk.chunk_data(data=_results, chunk_size=chunk_size)

        n_table = 0
        for _result in _results:
            if n_table == 0:
                table_1 = tabulate.tabulate(_result,
                                            colalign=('left', 'right', 'left'),
                                            maxcolwidths=[max_dt, max_bytes, new_max_path],
                                            headers=(f'[Modified]', '[Bytes]', f'[Files: {len(fp)}]'),
                                            stralign='left',
                                            tablefmt='f')
            else:
                table_1 = tabulate.tabulate(_result,
                                            colalign=('left', 'right', 'left'),
                                            maxcolwidths=[max_dt, max_bytes, new_max_path],
                                            stralign='left',
                                            tablefmt='plain')
            n_table += 1
            print(table_1)
            input()


def pre_scan_handler(_target: str, _verbose: bool, _recursive: bool) -> tuple:
    t = time.perf_counter()
    if _recursive is True:
        scan_results = scan(path=_target)
    else:
        scan_results = scan_depth_zero(path=_target)
    _files = scan_results[0]
    _x_files = scan_results[1]
    return _files, _x_files
