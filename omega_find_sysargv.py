import os
import sys
import ext_module
import string
import omega_find_banner
import omega_find_help
import handler_file
import asyncio
import get_path
import scanfs

program_root = get_path.get_path()


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
            if suffix_ == 'archive':
                suffix = ext_module.ext_archive
            elif suffix_ == 'audio':
                suffix = ext_module.ext_audio
            elif suffix_ == 'book':
                suffix = ext_module.ext_book
            elif suffix_ == 'code':
                suffix = ext_module.ext_code
            elif suffix_ == 'executable':
                suffix = ext_module.ext_executable
            elif suffix_ == 'font':
                suffix = ext_module.ext_font
            elif suffix_ == 'image':
                suffix = ext_module.ext_image
            elif suffix_ == 'sheet':
                suffix = ext_module.ext_sheet
            elif suffix_ == 'slide':
                suffix = ext_module.ext_slide
            elif suffix_ == 'text':
                suffix = ext_module.ext_text
            elif suffix_ == 'video':
                suffix = ext_module.ext_video
            elif suffix_ == 'web':
                suffix = ext_module.ext_web
        # custom suffix group
        elif '-csfx' in stdin:
            omega_find_banner.banner()
            print('-- searching for custom suffix groups ...')
            if os.path.exists(program_root+'\\suffix_group.txt'):
                custom_suffix_groups = []
                with open(program_root+'\\suffix_group.txt', 'r', encoding='utf8') as fo:
                    i = 0
                    for line in fo:
                        line = line.strip()
                        print(f'    [{i}] {line}')
                        custom_suffix_groups.append(line)
                        i += 1
                fo.close()
                print('')
                select_group = input('[Select Custom Suffix Group]: ')
                select_group = int(select_group.strip())
                if select_group in range(len(custom_suffix_groups)):
                    _sfx_group = custom_suffix_groups[select_group]
                    idx_sfx_name = _sfx_group.find(' ')
                    sfx_name = _sfx_group[:idx_sfx_name]
                    sfx_group = _sfx_group[idx_sfx_name+1:]
                    sfx_group = sfx_group.split(' ')
                    suffix = sfx_group
            else:
                print('-- no custom suffix groups found ...')
    return _mode, learn, de_scan, type_scan, p_scan, suffix, reveal_scan


def target(stdin: list, _mode) -> str:
    return stdin[stdin.index(_mode)+1]


def chunk_max(stdin: list) -> int:
    _chunk_max = 16
    if '--chunk-max' in stdin:
        _chunk_max = int(stdin[stdin.index('--chunk-max') + 1])
    return _chunk_max


def buffer_max(stdin: list) -> int:
    _buffer_max = 2048
    if '--buffer-max' in stdin:
        _buffer_max = int(stdin[stdin.index('--buffer-max')+1])
    return _buffer_max


def database(stdin: list) -> str:
    _db_recognized_files = program_root+'\\db\\database_file_recognition.txt'
    if not os.path.exists(program_root+'\\db\\database_file_recognition.txt'):
        open(program_root+'\\db\\database_file_recognition.txt', 'w').close()
    if '--database' in stdin:
        _db_recognized_files = stdin[stdin.index('--database')+1]
    return _db_recognized_files


def make_suffix_group():
    sfx_name = input('-- enter new a suffix group name (alpha numeric): ')
    valid_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    bool_valid_chars = True
    for char in sfx_name:
        if char not in valid_chars:
            bool_valid_chars = False
            print(f'-- invalid character: {char}')
            break
    if bool_valid_chars is True:
        sfx_group = input('-- enter suffix(s) (space delimited example: sh exe): ')
        print(f'-- new suffix group name: {sfx_name}')
        print(f'-- new suffix group: {sfx_group}')
        create_new_suffix_group = input('-- save?: ')
        if create_new_suffix_group == 'Y' or create_new_suffix_group == 'y':
            print('-- saving ...')
            if not os.path.exists(program_root+'\\suffix_group.txt'):
                open(program_root+'\\suffix_group.txt', 'w').close()
            with open(program_root+'\\suffix_group.txt', 'a', encoding='utf8') as fo:
                fo.write(sfx_name + ' ' + str(sfx_group) + '\n')
            print('-- done.')
            print('')


def clean_db(stdin: list) -> str:
    _db_recognized_files = program_root+'\\db\\database_file_recognition.txt'
    if '--database' in stdin:
        _db_recognized_files = stdin[stdin.index('--database')+1]
    return _db_recognized_files


def display_recognized(stdin: list) -> str:
    _db_recognized_files = program_root+'\\db\\database_file_recognition.txt'
    if '--database' in stdin:
        _db_recognized_files = stdin[stdin.index('--database')+1]
    return _db_recognized_files


def extract(stdin: list) -> bool:
    _extract = False
    if '--extract' in stdin:
        _extract = True
    return _extract


def verbosity(stdin: list) -> bool:
    verbose = False
    if '-v' in stdin:
        verbose = True
    return verbose


def loop_scandir_results(_list: list):
    try:
        usr_input = input('select? ')
        if usr_input.isdigit():
            usr_input = int(usr_input)
            result = _list[usr_input]
            idx = result.rfind('\\')
            fullpath = result[:idx]
            if usr_input <= len(_list):
                os.startfile(fullpath)
        loop_scandir_results(_list=_list)
    except KeyboardInterrupt:
        print('')
        pass


def run_and_exit(stdin: list):

    if os.path.exists(stdin[1]):
        omega_find_banner.banner()
        _path = stdin[1]
        _q = stdin[2]
        results = scanfs.search_scan(path=_path, q=_q)
        loop_scandir_results(_list=results)
        print('')

    elif '-h' in stdin:
        omega_find_help.omega_help()

    elif '--recognized' in stdin:
        omega_find_banner.banner()
        db_recognized_files = display_recognized(stdin)
        recognized_files, suffixes = asyncio.run(handler_file.read_definitions(fname=db_recognized_files))
        print(f'-- recognized file types: {len(recognized_files)}')
        print(f'-- recognized suffixes: {len(suffixes)}\n')

    elif '--new-suffix-group' in stdin:
        omega_find_banner.banner()
        make_suffix_group()

    else:
        return False
