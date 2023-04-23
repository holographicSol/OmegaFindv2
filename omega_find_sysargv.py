""" Written by Benjamin Jack Cullen """

import os
import variables_suffix
import string
import handler_file
import asyncio
import scanfs
import handler_print
import variable_paths
import handler_strings
import cli_character_limits
import tabulate
import tabulate_helper
import handler_post_process
import tabulate_helper2
import handler_chunk

program_root = variable_paths.get_executable_path()


def mode(stdin: list) -> tuple:
    # modes: learn, de-obfuscation, type-scan, password-protected-scan, reveal-scan.
    modes = ['-l', '-d', '-t', '-p', '-r', '-c', '-m']
    _mode = ''
    learn = False
    de_scan = False
    type_scan = False
    p_scan = False
    reveal_scan = False
    contents_scan = False
    mtime_scan = False
    suffix = []
    for m in modes:
        if m in stdin:
            _mode = m
    if _mode == '-l':
        learn = True
    elif _mode == '-c':
        contents_scan = True
    elif _mode == '-d':
        de_scan = True
    elif _mode == '-p':
        p_scan = True
    elif _mode == '-r':
        reveal_scan = True
    elif _mode == '-m':
        mtime_scan = True
    elif _mode == '-t':
        type_scan = True
        # suffix
        if '-sfx' in stdin:
            idx = stdin.index('-sfx')
            suffix.append(stdin[idx + 1].strip())
        # group suffix
        elif '-gsfx' in stdin:
            idx = stdin.index('-gsfx')
            suffix_ = stdin[idx + 1]
            suffix = variables_suffix.get_specified_suffix_group(suffix_)
        # custom suffix group
        elif '-csfx' in stdin:
            handler_print.display_searching_custom_suffix()
            handler_print.display_spacer()
            if os.path.exists(variable_paths.csfx_file_path):
                custom_suffix_groups = []
                with open(variable_paths.csfx_file_path, 'r', encoding='utf8') as fo:
                    i = 0
                    for line in fo:
                        line = line.strip()
                        handler_print.display_custom_suffix_result(i, line)
                        custom_suffix_groups.append(line)
                        i += 1
                fo.close()
                handler_print.display_spacer()
                select_group = handler_print.input_select()
                handler_print.display_spacer()
                select_group = int(select_group.strip())
                if select_group in range(len(custom_suffix_groups)):
                    _sfx_group = custom_suffix_groups[select_group]
                    idx_sfx_name = _sfx_group.find(' ')
                    sfx_name = _sfx_group[:idx_sfx_name]
                    sfx_group = _sfx_group[idx_sfx_name+1:]
                    sfx_group = sfx_group.split(' ')
                    suffix = sfx_group
            else:
                handler_print.display_no_custom_suffix()
    return _mode, learn, de_scan, type_scan, p_scan, suffix, reveal_scan, contents_scan, mtime_scan


def target(stdin: list, _mode) -> str:
    _target = str(stdin[stdin.index(_mode)+1]).strip()
    _target = _target.replace('"', '')
    _target = _target.replace("'", "")
    return _target


def recursive(stdin: list) -> bool:
    if '-R' in stdin:
        return True


def query(stdin: list) -> str:
    _query = ''
    if '-q' in stdin:
        idx = stdin.index('-q')+1
        i = 0
        for x in stdin:
            if i >= idx:
                _query = _query + ' ' + x
            i += 1
        _query = _query.strip()
    return _query


def chunk_max(stdin: list) -> int:
    _chunk_max = 16
    if '-cmax' in stdin:
        _chunk_max = int(stdin[stdin.index('-cmax') + 1])
    return _chunk_max


def buffer_max(stdin: list) -> int:
    _buffer_max = 2048
    if '-bmax' in stdin:
        _buffer_max = int(stdin[stdin.index('-bmax')+1])
    return _buffer_max


def vaild_chars(chars: str):
    valid_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '.' + '_' + '-'
    bool_valid_chars = True
    for char in chars:
        if char not in valid_chars:
            bool_valid_chars = False
            handler_print.display_invalid_char(char)
            break
    return bool_valid_chars


def database(stdin: list) -> str:
    _db_recognized_files = variable_paths.database_file_path
    handler_file.ensure_dir(variable_paths.database_dir_path)
    handler_file.ensure_db_file(variable_paths.database_file)
    if '-db' in stdin:
        _db_recognized_files = stdin[stdin.index('-db')+1]
        if vaild_chars(chars=_db_recognized_files) is True:
            handler_file.ensure_db_file(_db_recognized_files)
            _db_recognized_files = variable_paths.database_dir_path + _db_recognized_files
    return _db_recognized_files


def make_suffix_group():
    sfx_name = handler_print.input_custom_suffix_group_name()
    if vaild_chars(chars=sfx_name) is True:
        sfx_group = handler_print.input_custom_suffix()
        handler_print.display_new_custom_suffix_name(sfx_name)
        handler_print.display_new_custom_suffix_group(sfx_group)
        create_new_suffix_group = handler_print.input_save()
        if create_new_suffix_group == 'Y' or create_new_suffix_group == 'y':
            handler_print.display_saving()
            with open(variable_paths.csfx_file_path, 'a+', encoding='utf8') as fo:
                fo.write(sfx_name + ' ' + str(sfx_group) + '\n')
            handler_print.display_completed()


def display_recognized(stdin: list) -> str:
    _db_recognized_files = variable_paths.database_file_path
    if '-db' in stdin:
        _db_recognized_files = stdin[stdin.index('-db')+1]
    return _db_recognized_files


def extract(stdin: list) -> bool:
    _extract = False
    if '-e' in stdin:
        _extract = True
    return _extract


def verbosity(stdin: list) -> bool:
    verbose = False
    if '-v' in stdin:
        verbose = True
    return verbose


def interactive(stdin: list) -> bool:
    interact = True
    if '-I' in stdin:
        interact = False
    return interact


def sub_digits(stdin: list):
    _digits = True
    if '--digitless' in stdin:
        _digits = False
    return _digits


def sort_mode(stdin: list) -> str:
    _sort_mode = '--sort=file'

    if '--sort=mtime' in stdin:
        _sort_mode = '--sort=mtime'
    elif '--sort=buffer' in stdin:
        _sort_mode = '--sort=buffer'
    elif '--sort=size' in stdin:
        _sort_mode = '--sort=size'
    elif '--sort=file' in stdin:
        _sort_mode = '--sort=file'

    elif '--sort-reverse=mtime' in stdin:
        _sort_mode = '--sort-reverse=mtime'
    elif '--sort-reverse=buffer' in stdin:
        _sort_mode = '--sort-reverse=buffer'
    elif '--sort-reverse=size' in stdin:
        _sort_mode = '--sort-reverse=size'
    elif '--sort-reverse=file' in stdin:
        _sort_mode = '--sort-reverse=file'
    return _sort_mode


def write_bool(stdin: list) -> bool:
    _write_bool = False
    if '-O' in stdin:
        _write_bool = True
    return _write_bool


def loop_scandir_results(_list: list):
    try:
        handler_strings.input_open_dir(_list=_list)
        loop_scandir_results(_list=_list)
    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass


def human_size(stdin: list) -> bool:
    _human_size = False
    if '--human-size' in stdin:
        _human_size = True
    return _human_size


def dev_bench(stdin: list) -> bool:
    _bench = False
    if '--bench' in stdin:
        _bench = True
    return _bench


def run_and_exit(stdin: list, interact: bool, _sort_mode: str, human_size=False):

    if '-s' in stdin:
        _path = stdin[stdin.index('-s') + 1]
        if os.path.exists(_path):
            _q = stdin[stdin.index('-q') + 1]
            results = scanfs.search_scan(path=_path, q=_q, interact=interact, human_size=human_size,
                                         _sort_mode=_sort_mode)
            if interact is True:
                if results:
                    loop_scandir_results(_list=results)

    elif '-h' in stdin:
        handler_print.omega_help()

    elif '-XP' in stdin:
        db_recognized_files = display_recognized(stdin)
        recognized_files, suffixes = asyncio.run(handler_file.read_definitions(fname=db_recognized_files))
        handler_print.display_len_recognized_files(recognized_files)
        handler_print.display_len_recognized_suffixes(suffixes)

    elif '-A' in stdin:
        ext = stdin[stdin.index('-A') + 1]
        db_recognized_files = display_recognized(stdin)
        recognized_files, suffixes = asyncio.run(handler_file.read_definitions(fname=db_recognized_files))
        handler_print.display_associations(recognized_files, suffixes, ext, interact)

    elif '-AV' in stdin:
        db_recognized_files = display_recognized(stdin)
        recognized_files, suffixes = asyncio.run(handler_file.read_definitions(fname=db_recognized_files))
        handler_print.display_all_associations(recognized_files, suffixes, interact)

    elif '-G' in stdin:
        suffix_group_name = stdin[stdin.index('-G') + 1]
        handler_print.show_suffix_group(suffix_group_name)

    elif '-L' in stdin:

        # get report files
        i = 0
        fp = []
        for dirName, subdir, filelist in os.walk(variable_paths.data_dir_path):
            for fname in filelist:
                if fname.endswith('.txt') and 'pre_scan' not in fname:
                    fp.append([i, os.path.join(dirName, fname)])
                    i += 1

        # display report files
        if fp:
            chunk_size = 2
            tabulate.PRESERVE_WHITESPACE = True

            max_column_width = cli_character_limits.column_width_from_shutil(n=2, reduce=0)

            max_0 = handler_post_process.longest_item(fp, idx=0)
            _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=fp,
                                                                             col_idx=0,
                                                                             max_column_width=max_0,
                                                                             padding_left=False)

            _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                             col_idx=1,
                                                                             max_column_width=max_column_width,
                                                                             padding_left=False)

            max_column_width_tot = max_column_width * 2
            new_max_path = max_column_width_tot - max_0 - 2

            _results = handler_chunk.chunk_data(data=_results, chunk_size=chunk_size)

            n_table = 0
            for _result in _results:

                if n_table == 0:
                    table_1 = tabulate.tabulate(_result,
                                                maxcolwidths=[max_0, new_max_path],
                                                headers=(f'Index', f'Files: {len(fp)}'),
                                                stralign='left')
                else:
                    table_1 = tabulate.tabulate(_result,
                                                maxcolwidths=[max_0, new_max_path],
                                                headers=(f'Index', f'Files: {len(fp)}'),
                                                stralign='left',
                                                tablefmt='plain')

                print(table_1)

                if interact is True:
                    print('')
                    f = input('select: ')
                    if f and f.isdigit():
                        asyncio.run(handler_file.read_report(fname=fp[int(f)][1]))
                        break
                    print('')

                n_table += 1

    elif '-nsfx' in stdin:
        make_suffix_group()

    else:
        return False
