""" Written by Benjamin Jack Cullen """

import tabulate

import handler_chunk
import power_time
import cli_character_limits
import variables_suffix


# ------------------------------------------------------------------------------> banner

def banner():
    print('')
    print('')
    print('[OmegaFind v2] Forensics tool. Search differently.')
    print('')


# ------------------------------------------------------------------------------> help

def omega_help():
    banner()
    print(' -l       Learn                 Specify location to learn from.')
    print(' -r       Reveal                Display all file types.')
    print(' -p       Password Protected    Only scan for password protected archives.')
    print(' -d       De-Obfuscation        Attempt to find files where suffix does not match contents.')
    print(' -t       Type                  Display all files of type.')
    print(' -sfx     Suffix                Specify suffix. Used with -t.')
    print(' -csfx    Custom Suffix         Specify custom suffix group. Used with -t.')
    print(' -gsfx    Group Suffix          Specify default group suffix group. Used with -t.')
    print('                                archive, audio, book, code, exe, font, image, sheet, slide, text, video, web.')
    print(' -nsfx    New Suffix Group      Create new custom suffix group.')
    print(' -e       Extract               Attempt to extract archive while scanning.')
    print(' -db      Database              Specify database to use while learning/scanning.')
    print(' -cmax    Chunk Max             Specify in digits max items to be processed at any one time.')
    print(' -bmax    Buffer Max            Specify in digits maximum number of bytes to read of each file.')
    print(' -C       Compatible            Display specified suffix group.')
    print(' -I       Interact              Disables interaction. No prompt mode.')
    print(' -R       Recognized            Display current learning XP.')
    print('')
    print(' -v       Verbosity             Increase verbosity.')
    print(' -h       Help                  Display this help message.')
    print('')
    print(' [Author] Developed and written by Benjamin Jack Cullen.')


# ------------------------------------------------------------------------------> exceptions

def display_exception(_msg: str, e: Exception):
    print(_msg, e)


# ------------------------------------------------------------------------------> mode
def display_mode(_verbose: bool, _mode: str):
    if _verbose is True:
        if _mode == '-l':
            print('Mode: Learning\n\n')
        elif _mode == '-d':
            print('Mode: Deobfuscation\n\n')
        elif _mode == '-t':
            print('Mode: Type Scan\n\n')
        elif _mode == '-p':
            print('Mode: Password Scan\n\n')
        elif _mode == '-r':
            print('Mode: Reveal Scan\n\n')


# ------------------------------------------------------------------------------> results

def display_prescan_info(_files, _x_files, completion_time):
    max_column_width = cli_character_limits.column_width_from_tput(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(completion_time))
    print(tabulate.tabulate([[*[len(_files)], *[len(_x_files)], *[scan_time_human]]],
                            maxcolwidths=[max_column_width, max_column_width],
                            headers=('Pre-Scan Files            ', 'Errors                ', 'Time                  '),
                            stralign='right'))
    print('')
    print('')


def display_reveal_scan_results_overview(_results, _exc, _t_completion):
    print(f'Found {len(_results)} files (errors: {len(_exc)}). time: {_t_completion}\n')


def display_de_scan_results_overview(_results, _exc, _t_completion):
    print(f'Found {len(_results)} unrecognized or obfuscated files (errors: {len(_exc)}). time: {_t_completion}\n')


def display_type_scan_results_overview(_results, _exc, _t_completion):
    print(f'Found {len(_results)} files (errors: {len(_exc)}). time: {_t_completion}\n')


def display_p_scan_results_overview(_results, _exc, _t_completion):
    print(f'Found {len(_results)} password protected files (errors: {len(_exc)}). time: {_t_completion}\n')


def display_more_results_available():
    print(' More results available in results file.')


def display_search_scan_result(i_match, p):
    print(f'[{i_match}] {p}')


def display_zero_results(_results, _t_completion, _exc, _header_0):
    _results = []
    max_column_width = cli_character_limits.column_width_from_tput(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
    table_0 = tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                                maxcolwidths=[max_column_width, max_column_width],
                                headers=(f'{_header_0}', 'Errors                ', 'Time                  '),
                                stralign='right')
    print(table_0)


# ------------------------------------------------------------------------------> invalid
def display_invalid_input():
    print('-- invalid input')


def display_invalid_path(path):
    print(f'-- invalid path: {path}')


def display_invalid_database(path):
    print(f'-- invalid database: {path}')


def display_invalid_char(char):
    print(f'-- invalid character: {char}')


# ------------------------------------------------------------------------------> custom suffix

def display_searching_custom_suffix():
    print('custom suffix groups:')


def display_custom_suffix_result(i, item):
    print(f'[{i}] {item}')


def display_no_custom_suffix():
    print('-- no custom suffix groups found ...')


def display_new_custom_suffix_name(sfx_name):
    print(f'-- new suffix group name: {sfx_name}')


def display_new_custom_suffix_group(sfx_group):
    print(f'-- new suffix group name: {sfx_group}')


def display_suffixes(_msg: str, _list: list):
    print(_msg)
    print('')
    chunks = handler_chunk.chunk_data(data=_list, chunk_size=6)
    print(tabulate.tabulate(chunks, tablefmt='plain'))


def show_suffix_group(suffix_group_name: str):
    suffix = variables_suffix.get_specified_suffix_group(suffix_group_name)
    display_suffixes(_msg=f'[Suffix Group Compatibility ({suffix_group_name})]',
                     _list=suffix)


def default_suffix_group_compat():
    i = 0
    for ext_group in variables_suffix.ext_list:
        print('')
        print(f'[Suffix Group Compatibility ({variables_suffix.ext_name[i]})]')
        print('')
        chunks = handler_chunk.chunk_data(data=ext_group, chunk_size=6)
        print(tabulate.tabulate(chunks, tablefmt='plain'))
        print('')
        i += 1


# ------------------------------------------------------------------------------> saving

def display_saving():
    print('-- saving ...')


# ------------------------------------------------------------------------------> completed

def display_completed():
    print('-- done.')


# ------------------------------------------------------------------------------> xp

def display_len_recognized_files(recognized_files):
    print(f' Recognized file types: {len(recognized_files)}')


def display_len_recognized_suffixes(suffixes):
    print(f' Recognized suffixes:   {len(suffixes)}')


# ------------------------------------------------------------------------------> spacer

def display_spacer():
    print('')


# ------------------------------------------------------------------------------> input

def input_custom_suffix_group_name() -> str:
    return input('-- enter new a suffix group name (alpha numeric): ')


def input_custom_suffix() -> str:
    return input('-- enter suffix(s) (space delimited example: sh exe): ')


def input_save() -> str:
    return input('-- save?: ')


def input_select() -> str:
    return input(': ')
