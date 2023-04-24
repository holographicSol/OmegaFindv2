""" Written by Benjamin Jack Cullen """
import os

import tabulate
import handler_post_process
import handler_chunk
import power_time
import cli_character_limits
import variables_suffix
import variable_paths
import tabulate_helper2
import handler_input

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
    print(' -c       Contents Scan         Specify a directory in which file contents will be scanned.')
    print(' -d       De-Obfuscation        Attempt to find files where suffix does not match contents.')
    print(' -p       Password Protected    Only scan for password protected archives.')
    print(' -r       Reveal Scan           Display all file types.')
    print(' -t       Type Scan             Display all files of type.')
    print(' -m       Modified Time Scan    Display modified time for all files.')
    print(' -s       String Scan           Display all files containing string. Used with -q.')
    print(' -q       Query                 Specify a search query. Used with -c. -c PATH -q QUERY.')
    print(' -sfx     Suffix                Specify suffix. Used with -t.')
    print(' -csfx    Custom Suffix         Specify custom suffix group. Used with -t.')
    print(' -gsfx    Group Suffix          Specify default suffix group. Used with -t.')
    print(' -nsfx    New Suffix Group      Create new custom suffix group.')
    print('                                archive, audio, book, code, exe, font, image, sheet, slide, text, video, web.')
    print('')
    print(' -db      Database              Specify database to use while learning/scanning.')
    print(' -e       Extract               Attempt archive extraction while scanning.')
    print(' -bmax    Buffer Max            Specify in digits maximum number of bytes to read of each file.')
    print(' -cmax    Chunk Max             Specify in digits max chunk size.')
    print('')
    print(' -A       Associations          Display buffer associations to specified suffix.')
    print(' -AV      All Associations      Display all known suffix buffer associations.')
    print(' -G       Group                 Display specified suffix group.')
    print(' -I       Interact              Disables interaction. No prompt mode.')
    print(' -L       List Scan Reports     List and select previously completed scan report.')
    print(' -O       Write Output          Save logging and results to file. Takes no further arguments.')
    print(' -R       Recursive             Scan directories recursively. (Scans all sub-directories).')
    print(' -XP      Experience            Display how many associations have been learned.')
    print('')
    print(' --digitless                    Omit versioning,timestamps,dimensions etc. when comparing magic buffers.')
    print(' --human-size                   Display bytes in human sizes.')
    print(' --sort=mtime                   Sort by Modified Time')
    print(' --sort=buffer                  Sort by Buffer')
    print(' --sort=size                    Sort by Size')
    print(' --sort=file                    Sort by Filename')
    print(' --sort-reverse=mtime           Sort by Modified Time')
    print(' --sort-reverse=buffer          Sort by Buffer')
    print(' --sort-reverse=size            Sort by Size')
    print(' --sort-reverse=file            Sort by Filename')
    print(' --csfx-remove                  Specify a custom suffix group to be removed.')
    print('')
    print(' -v       Verbosity             Increase verbosity.')
    print(' -h       Help                  Display this help message.')
    print('')
    print('[Author] Developed and written by Benjamin Jack Cullen.')


# ------------------------------------------------------------------------------> exceptions

def display_exception(_msg: str, e: Exception):
    print(_msg, e)


# ------------------------------------------------------------------------------> results

def display_zero_results(_results, _t_completion, _exc, _header_0):
    _results = []
    max_column_width = cli_character_limits.column_width_from_shutil(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
    table_0 = tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                                maxcolwidths=[max_column_width, max_column_width, max_column_width],
                                headers=(f'{_header_0}', 'Errors                ', 'Time                  '),
                                stralign='right')
    print(table_0)


# ------------------------------------------------------------------------------> invalid
def display_invalid_input():
    print('invalid input')


def display_invalid_path(path):
    print(f'invalid path: {path}')


def display_invalid_database(path):
    print(f'invalid database: {path}')


def display_invalid_char(char):
    print(f'invalid character: {char}')


# ------------------------------------------------------------------------------> custom suffix

def display_searching_custom_suffix():
    print('custom suffix groups:')


def display_custom_suffix_result(i, item):
    print(f'[{i}] {item}')


def display_no_custom_suffix():
    print('no custom suffix groups found ...')


def display_new_custom_suffix_name(sfx_name):
    print(f'new suffix group name: {sfx_name}')


def display_new_custom_suffix_group(sfx_group):
    print(f'new suffix group name: {sfx_group}')


def display_suffixes(_msg: str, _list: list):
    print(_msg)
    print('Suffix Group:\n')
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
        display_suffixes(_msg=f'Suffix Group Name: {suffix_group_name}', _list=suffix)


def show_custom_suffix_group_names():
    if os.path.exists(variable_paths.csfx_file_path):
        group_names = []
        with open(variable_paths.csfx_file_path, 'r', encoding='utf8') as fo:
            for line in fo:
                line = line.strip()
                line = line.split(' ')
                group_names.append(line[0])
        fo.close()
        if group_names:
            return group_names


def display_associations(recognized_files: list, suffixes: list, ext: str, interact: bool):
    _results = []
    for recognized in recognized_files:
        if str(recognized[0]).strip() == str(ext).strip():
            _results.append(recognized)

    if _results:
        # enumeration for reasonable column widths
        chunk_size = 40
        tabulate.PRESERVE_WHITESPACE = True

        max_column_width = cli_character_limits.column_width_from_shutil(n=2)

        max_0 = handler_post_process.longest_item(recognized_files, idx=0)
        _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                         col_idx=0,
                                                                         max_column_width=max_0,
                                                                         padding_left=True)

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
                                            colalign=('left', 'left'),
                                            maxcolwidths=[max_0, new_max_path],
                                            headers=('Ext.', f'Learned Associations: {len(recognized_files)}'),
                                            stralign='left')
            else:
                table_1 = tabulate.tabulate(_result,
                                            colalign=('left', 'left'),
                                            maxcolwidths=[max_0, new_max_path],
                                            stralign='left',
                                            tablefmt='plain')

            print(table_1)
            n_table += 1
            if interact is True:
                if not _result == _results[-1]:
                    try:
                        handler_input.input_singularity(message='')
                    except KeyboardInterrupt:
                        print('logging: keyboard interrupt')
                        break
                    except:
                        pass


def display_all_associations(recognized_files: list, suffixes: list, interact: bool):

    if recognized_files:
        # enumeration for reasonable column widths
        chunk_size = 40
        tabulate.PRESERVE_WHITESPACE = True

        max_column_width = cli_character_limits.column_width_from_shutil(n=2)

        max_0 = handler_post_process.longest_item(recognized_files, idx=0)
        _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=recognized_files,
                                                                         col_idx=0,
                                                                         max_column_width=max_0,
                                                                         padding_left=True)

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
                                            colalign=('left', 'left'),
                                            headers=('Ext.', f'Learned Associations: {len(recognized_files)}'),
                                            maxcolwidths=[max_0, new_max_path],
                                            stralign='left')
            else:
                table_1 = tabulate.tabulate(_result,
                                            colalign=('left', 'left'),
                                            maxcolwidths=[max_0, new_max_path],
                                            stralign='left',
                                            tablefmt='plain')

            print(table_1)
            n_table += 1
            if interact is True:
                try:
                    handler_input.input_singularity(message='')
                except KeyboardInterrupt:
                    break


# ------------------------------------------------------------------------------> saving

def display_saving():
    print('saving ...')


# ------------------------------------------------------------------------------> completed

def display_completed():
    print('done.')


# ------------------------------------------------------------------------------> xp

def display_len_recognized_files(recognized_files):
    print(f'Recognized file types: {len(recognized_files)}')


def display_len_recognized_suffixes(suffixes):
    print(f'Recognized suffixes:   {len(suffixes)}')


# ------------------------------------------------------------------------------> spacer

def display_spacer():
    print('')
