""" Written by Benjamin Jack Cullen """

import tabulate
import handler_post_process
import handler_chunk
import power_time
import cli_character_limits
import variables_suffix
import tabulate_helper
import variable_paths


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
    print(' -d       De-Obfuscation        Attempt to find files where suffix does not match contents.')
    print(' -p       Password Protected    Only scan for password protected archives.')
    print(' -r       Reveal                Display all file types.')
    print(' -t       Type                  Display all files of type.')
    print(' -sfx     Suffix                Specify suffix. Used with -t.')
    print(' -csfx    Custom Suffix         Specify custom suffix group. Used with -t.')
    print(' -gsfx    Group Suffix          Specify default suffix group. Used with -t.')
    print('                                archive, audio, book, code, exe, font, image, sheet, slide, text, video, web.')
    print('')
    print(' -db      Database              Specify database to use while learning/scanning.')
    print(' -e       Extract               Attempt archive extraction while scanning.')
    print(' -bmax    Buffer Max            Specify in digits maximum number of bytes to read of each file.')
    print(' -cmax    Chunk Max             Specify in digits max items to be processed at any one time.')
    print(' -nsfx    New Suffix Group      Create new custom suffix group.')
    print('')
    print(' -A       Associations          Display buffer associations to specified suffix.')
    print(' -AV      All Associations      Display all known suffix buffer associations.')
    print(' -G       Group                 Display specified suffix group.')
    print(' -I       Interact              Disables interaction. No prompt mode.')
    print(' -L       List Scan Reports     List and select previously completed scan report.')
    print(' -R       Recognized            Display current learning XP.')
    print('')
    print(' -v       Verbosity             Increase verbosity.')
    print(' -h       Help                  Display this help message.')
    print('')
    print('[Author] Developed and written by Benjamin Jack Cullen.')


# ------------------------------------------------------------------------------> exceptions

def display_exception(_msg: str, e: Exception):
    print(_msg, e)


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


def display_zero_results(_results, _t_completion, _exc, _header_0):
    _results = []
    max_column_width = cli_character_limits.column_width_from_tput(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
    table_0 = tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                                maxcolwidths=[max_column_width, max_column_width, max_column_width],
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
    if suffix is None:
        suffix = []
        with open(variable_paths.csfx_file_path, 'r', encoding='utf8') as fo:
            i = 0
            for line in fo:
                line = line.strip()
                if line.startswith(suffix_group_name):
                    line = line.split(' ')
                    line.remove(line[0])
                    suffix = line
                i += 1
        fo.close()
    if suffix:
        display_suffixes(_msg=f'[ Suffix Group: {suffix_group_name} ]', _list=suffix)


def display_associations(recognized_files: list, suffixes: list, ext: str, interact: bool):
    table_list = []
    for recognized in recognized_files:
        if str(recognized[0]).strip() == str(ext).strip():
            table_list.append(recognized)

    if table_list:
        # enumeration for reasonable column widths
        max_column_width = cli_character_limits.column_width_from_tput(n=2)
        max_column_width_tot = max_column_width * 2
        max_0 = handler_post_process.longest_item(table_list, idx=0)
        new_max_path = max_column_width_tot - max_0 - 1

        table_0 = tabulate.tabulate(*[table_list],
                                    maxcolwidths=[max_0, new_max_path],
                                    headers=('Ext.', f'Buffers [{len(table_list)}/{len(recognized_files)}]'),
                                    stralign='left')
        # display results tale
        if interact is True:
            tabulate_helper.display_rows_interactively(max_limit=75,
                                                       results=table_list,
                                                       table=table_0,
                                                       extra_input=False,
                                                       message='\n-- more --\n',
                                                       function=None)
        else:
            print(table_0)


def display_all_associations(recognized_files: list, suffixes: list, interact: bool):

    if recognized_files:
        # enumeration for reasonable column widths
        max_column_width = cli_character_limits.column_width_from_tput(n=2)
        max_column_width_tot = max_column_width * 2
        max_0 = handler_post_process.longest_item(recognized_files, idx=0)
        new_max_path = max_column_width_tot - max_0 - 1

        table_0 = tabulate.tabulate(*[recognized_files],
                                    headers=('Ext.', f'Buffers [{len(recognized_files)}]'),
                                    maxcolwidths=[max_0, new_max_path],
                                    stralign='left')
        # display results tale
        if interact is True:
            tabulate_helper.display_rows_interactively(max_limit=75,
                                                       results=recognized_files,
                                                       table=table_0,
                                                       extra_input=False,
                                                       message='\n-- more --\n',
                                                       function=None)
        else:
            print(table_0)


# ------------------------------------------------------------------------------> saving

def display_saving():
    print('-- saving ...')


# ------------------------------------------------------------------------------> completed

def display_completed():
    print('-- done.')


# ------------------------------------------------------------------------------> xp

def display_len_recognized_files(recognized_files):
    print(f'Recognized file types: {len(recognized_files)}')


def display_len_recognized_suffixes(suffixes):
    print(f'Recognized suffixes:   {len(suffixes)}')


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
