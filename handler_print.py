""" Written by Benjamin Jack Cullen """


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
    print(' -R       Recognized            Display current learning XP.')
    print('')
    print(' -v       Verbosity             Increase verbosity.')
    print(' -h       Help                  Display this help message.')
    print('')
    print(' [Author] Developed and written by Benjamin Jack Cullen.')
    print('')


# ------------------------------------------------------------------------------> exceptions

def display_exception(_msg: str, e: Exception):
    print(_msg, e)


# ------------------------------------------------------------------------------> results

def display_prescan_info(_files, _x_files, completion_time):
    print(f' Found {len(_files)} files during pre-scan (errors: {len(_x_files)}). time: {completion_time}')


def display_reveal_scan_results_overview(_results, _exc, _t_completion):
    print(f' Found {len(_results)} files (errors: {len(_exc)}). time: {_t_completion}')


def display_result(_item):
    print(*_item)


def display_results_header_de_scan():
    print('')
    # print('\n'+str('Unrecognized:'))


def display_results_header_type_scan():
    print('')
    # print('\n'+str('Found:'))


def display_results_header_pscan():
    print('')
    # print('\n'+str('Password protected:'))


def display_results_header_reveal_scan():
    print('')
    # print('\n'+str('Found:'))


def display_more_results_available():
    print(' More results available in results file.')


def display_learning_results_overview(_results):
    print(f' New definitions: {len(_results)}')
    print('  Updating definitions ..')


def display_de_scan_results_overview(_results, _exc, _t_completion):
    print('')
    # print(f' Found {len(_results)} unrecognized or obfuscated files (errors: {len(_exc)}). time: {_t_completion}')


def display_type_scan_results_overview(_results, _exc, _t_completion):
    print('')
    # print(f' Found {len(_results)} files (errors: {len(_exc)}). time: {_t_completion}')


def display_p_scan_results_overview(_results, _exc, _t_completion):
    print('')
    # print(f' Found {len(_results)} password protected files (errors: {len(_exc)}). time: {_t_completion}')


def display_search_scan_result(i_match, p):
    print(f'[?][{i_match}] {p}')


def display_zero_results(_exc):
    print(f' Zero results (errors: {len(_exc)}).')


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
    for _ in _list:
        print('    ' + str(_))


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
    print(f' Recognized suffixes:   {len(suffixes)}\n')


# ------------------------------------------------------------------------------> spacer

def display_spacer():
    print('')


# ------------------------------------------------------------------------------> input

def input_custom_suffix_group_name():
    return input('-- enter new a suffix group name (alpha numeric): ')


def input_custom_suffix():
    return input('-- enter suffix(s) (space delimited example: sh exe): ')


def input_save():
    return input('-- save?: ')


def input_select():
    return input(': ')
