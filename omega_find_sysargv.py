import os
import sys
import ext_module
import string


def mode():

    modes = ['--learn', '--de-scan', '--type-scan']
    _mode = ''
    learn = False
    de_scan = False
    type_scan = False
    suffix = []
    for m in modes:
        if m in sys.argv:
            _mode = m
    if _mode == '--learn':
        learn = True
    elif _mode == '--de-scan':
        de_scan = True
    elif _mode == '--type-scan':
        type_scan = True
        if '--suffix' in sys.argv:
            idx = sys.argv.index('--suffix')
            suffix.append(sys.argv[idx + 1].strip())
        elif '--group-suffix' in sys.argv:
            idx = sys.argv.index('--group-suffix')
            suffix_ = sys.argv[idx + 1]
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
        elif '--custom-suffix' in sys.argv:
            print('\n[OmegaFind v2]')
            print('[Searching for Custom Suffix Groups] ..')
            if os.path.exists('./suffix_group.txt'):
                custom_suffix_groups = []
                with open('./suffix_group.txt', 'r', encoding='utf8') as fo:
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
                    print(f'    [Suffix Group Name] {sfx_name}')
                    print(f'    [Suffix Group] {sfx_group}')
                    suffix = sfx_group
                    print('')
            else:
                print('[Did not find any Custom Suffix Groups] ..')
                print('')

    return _mode, learn, de_scan, type_scan, suffix


def target(mode) -> str:
    return sys.argv[sys.argv.index(mode) + 1]


def chunk_max() -> int:
    _chunk_max = 16
    if '--chunk-max' in sys.argv:
        _chunk_max = int(sys.argv[sys.argv.index('--chunk-max') + 1])
    return _chunk_max


def buffer_max() -> int:
    _buffer_max = 1024
    if '--buffer-max' in sys.argv:
        _buffer_max = int(sys.argv[sys.argv.index('--buffer-max')+1])
    return _buffer_max


def database() -> str:
    _db_recognized_files = './db/database_file_recognition.txt'
    if '--database' in sys.argv:
        _db_recognized_files = sys.argv[sys.argv.index('--database')+1]
    return _db_recognized_files


def make_suffix_group():
    sfx_name = input('[Enter new suffix group name (alpha numeric)]: ')
    valid_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    bool_valid_chars = True
    for char in sfx_name:
        if char not in valid_chars:
            bool_valid_chars = False
            print(f'[Invalid Character] {char}')
            break
    if bool_valid_chars is True:
        sfx_group = input('[Enter suffix(s) (space delimited example: sh exe)]: ')
        sfx_group = sfx_group.split(' ')
        print(f'[New Suffix Group Name] {sfx_name}')
        print(f'[New Suffix Group] {sfx_group}')
        create_new_suffix_group = input('[Save?]: ')
        if create_new_suffix_group == 'Y' or create_new_suffix_group == 'y':
            print('[Saving] ..')
            if not os.path.exists('./suffix_group.txt'):
                open('./suffix_group.txt', 'w').close()
            with open('./suffix_group.txt', 'a', encoding='utf8') as fo:
                fo.write(sfx_name + ' ' + str(sfx_group) + '\n')
            print('[Done]')
            print('')


def clean_db() -> str:
    _db_recognized_files = './db/database_file_recognition.txt'
    if '--database' in sys.argv:
        _db_recognized_files = sys.argv[sys.argv.index('--database')+1]
    return _db_recognized_files


def verbosity() -> bool:
    verbose = False
    if '-v' in sys.argv:
        verbose = True
    return verbose
