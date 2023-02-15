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

program_root = variable_paths.get_executable_path()


def mode(stdin: list) -> tuple:
    # modes: learn, de-obfuscation, type-scan, password-protected-scan, reveal-scan.
    modes = ['-l', '-d', '-t', '-p', '-r']
    _mode = ''
    learn = False
    de_scan = False
    type_scan = False
    p_scan = False
    reveal_scan = False
    suffix = []
    for m in modes:
        if m in stdin:
            _mode = m
    if _mode == '-l':
        learn = True
    elif _mode == '-d':
        de_scan = True
    elif _mode == '-p':
        p_scan = True
    elif _mode == '-r':
        reveal_scan = True
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
    return _mode, learn, de_scan, type_scan, p_scan, suffix, reveal_scan


def target(stdin: list, _mode) -> str:
    return stdin[stdin.index(_mode)+1]


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
            if not os.path.exists(variable_paths.csfx_file_path):
                open(variable_paths.csfx_file_path, 'w').close()
            with open(variable_paths.csfx_file_path, 'a', encoding='utf8') as fo:
                fo.write(sfx_name + ' ' + str(sfx_group) + '\n')
            handler_print.display_completed()


def clean_db(stdin: list) -> str:
    _db_recognized_files = variable_paths.database_dir_path
    if '-db' in stdin:
        _db_recognized_files = stdin[stdin.index('-db')+1]
    return _db_recognized_files


def display_recognized(stdin: list) -> str:
    _db_recognized_files = variable_paths.database_dir_path
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


def loop_scandir_results(_list: list):
    try:
        handler_strings.input_open_dir(_list=_list)
        loop_scandir_results(_list=_list)
    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass


def run_and_exit(stdin: list, interact: bool):

    if os.path.exists(stdin[1]):
        _path = stdin[1]
        _q = stdin[2]
        results = scanfs.search_scan(path=_path, q=_q, interact=interact)
        loop_scandir_results(_list=results)

    elif '-h' in stdin:
        handler_print.omega_help()

    elif '-R' in stdin:
        db_recognized_files = display_recognized(stdin)
        recognized_files, suffixes = asyncio.run(handler_file.read_definitions(fname=db_recognized_files))
        handler_print.display_len_recognized_files(recognized_files)
        handler_print.display_len_recognized_suffixes(suffixes)

    elif '-SGSFX' in stdin:
        suffix_group_name = stdin[stdin.index('-SGSFX') + 1]
        handler_print.show_suffix_group(suffix_group_name)

    elif '-nsfx' in stdin:
        make_suffix_group()

    else:
        return False
