""" Written by Benjamin Jack Cullen """

import asyncio

import handler_chunk
import handler_file
import handler_post_process
import handler_print
import tabulate
import cli_character_limits
import power_time
import time
import tabulate_helper2
import handler_convert_results


def learn_result_handler_display(_results: list, _exc: list, _t_completion: str, _verbose: bool):
    max_column_width = cli_character_limits.column_width_from_shutil(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
    print(tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                            maxcolwidths=[max_column_width, max_column_width, max_column_width],
                            headers=('Learned                   ', 'Errors                ', 'Time                  '),
                            stralign='right'))


def result_handler_display(_results: list, _exc: list, _t_completion: str, _verbose: bool,
                           _de_scan_bool: bool, _type_scan_bool: bool, _p_scan: bool,
                           _reveal_scan: bool, _dt: str, _header_0: str,
                           interact: bool, _contents_scan: bool, write_bool: bool, _mtime_scan: bool,
                           _bench: bool, _query='', _human_size=False):
    if len(_results) >= 1:

        # create filename
        part_fname = 'scan_results_'
        if _de_scan_bool is True:
            part_fname = 'de_scan'
        elif _type_scan_bool is True:
            part_fname = 'type_scan'
        elif _p_scan is True:
            part_fname = 'pscan'
        elif _reveal_scan is True:
            part_fname = 'reveal_scan'
        elif _contents_scan is True:
            part_fname = 'contents_scan'
        elif _mtime_scan is True:
            part_fname = 'mtime_scan'

        # convert timestamps to datetime: do not do this before sorting (omega_findv2.py).
        _results = handler_convert_results.convert_results(_results, _human_size=_human_size, _mtime_scan=_mtime_scan)

        # create table for file: each entry should be on one line for ease of parsing.
        if write_bool is True:
            if _mtime_scan is False:
                table_file = tabulate.tabulate(_results,
                                               colalign=('left', 'right', 'right', 'left'),
                                               headers=('Modified', f'Buffer [{_header_0}]', 'Bytes',
                                                        f'Files: {len(_results)}    Errors: {len(_exc)}'),
                                               stralign='left')
            else:
                table_file = tabulate.tabulate(_results,
                                               colalign=('left', 'right', 'left'),
                                               headers=(
                                                   'Modified', 'Bytes', f'Files: {len(_results)}    Errors: {len(_exc)}'),
                                               stralign='left')
            asyncio.run(handler_file.write_scan_results(table_file, file=part_fname + '_' + _dt + '.txt', _dt=_dt))

        # create table to be displayed:
        # tabulation in stages to greatly reduce tabulation time which was exceeding a 3rd of main operation time
        _results_len = len(_results)
        chunk_size = 75

        if interact is True:
            if _bench is True:
                t0 = time.perf_counter()

            # a little tampering with tabulate to preserve the padding
            tabulate.PRESERVE_WHITESPACE = True
            if _mtime_scan is False:

                # Let's produce the max_column_width alignment of one big table but with the speed of producing one
                # tiny table. The best of both worlds.
                # also i will be aligning buffers right and file paths left wit a stem of bytes for art.

                # divide the number of characters that fit on the screen (fit at this very point in time) by N columns.
                max_column_width = cli_character_limits.column_width_from_shutil(n=4)

                # tabulate is great at creating new lines based on max_column_width however tabulate will also honour
                # existing new lines and whitespace if instructed to do so.
                # tabulate helper max_column_width=None = use max data length found at col_idx in each sublist.
                # tabulate helper max_column_width=xyz = specify a max_column_width
                _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                                 col_idx=2,
                                                                                 max_column_width=None)

                # again for the next column of variable data lengths.
                _results = tabulate_helper2.add_padding_and_new_lines_to_columns(data=_results,
                                                                                 col_idx=1,
                                                                                 max_column_width=max_column_width)

                # enumerate remaining column widths
                max_column_width_tot = max_column_width * 4
                max_dt = handler_post_process.longest_item(_results, idx=0)
                max_bytes = handler_post_process.longest_item(_results, idx=2)
                new_max_path = max_column_width_tot - max_dt - max_column_width - max_bytes - 8

                # chunk results by a reasonable number so as not to flood the console and loose results (interactive)
                _results = handler_chunk.chunk_data(data=_results, chunk_size=chunk_size)

                if _bench is True:
                    print(f'pre-tabulation time: {time.perf_counter()-t0}')
                    print('')

                # tabulate a tiny table (fast) rather than a huge table (potentially slow) while retaining maxcolwidths
                # consistently through each tiny table. now tabulate only calculates maxcolwidths for one tiny
                # table at a time (which is faster than tabulate calculating maxcolwidths for one huge table) and we
                # keep table maxcolwidths alignment from one table to the next.
                n_table = 0
                for _result in _results:
                    if n_table == 0:
                        table_1 = tabulate.tabulate(_result,
                                                    colalign=('left', 'right', 'right', 'left'),
                                                    maxcolwidths=[max_dt, None, max_bytes, new_max_path],
                                                    headers=('[Modified]', f'[Buffer: {_header_0.replace(": "+_query, "")}]', '[Bytes]', f'[Files: {_results_len}    Errors: {len(_exc)}]'),
                                                    stralign='left',
                                                    floatfmt='f')
                    else:
                        table_1 = tabulate.tabulate(_result,
                                                    colalign=('left', 'right', 'right', 'left'),
                                                    maxcolwidths=[max_dt, None, max_bytes, new_max_path],
                                                    stralign='left',
                                                    tablefmt='plain',
                                                    floatfmt='f')
                    print(table_1)
                    n_table += 1
                    try:
                        input()
                    except KeyboardInterrupt:
                        break
            else:
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

                if _bench is True:
                    print(f'pre-tabulation time: {time.perf_counter()-t0}')
                    print('')

                n_table = 0
                for _result in _results:
                    if n_table == 0:
                        table_1 = tabulate.tabulate(_result,
                                                    colalign=('left', 'right', 'left'),
                                                    maxcolwidths=[max_dt, max_bytes, new_max_path],
                                                    headers=('[Modified]', '[Bytes]', f'[Files: {_results_len}    Errors: {len(_exc)}]'),
                                                    stralign='left')
                    else:
                        table_1 = tabulate.tabulate(_result,
                                                    colalign=('left', 'right', 'left'),
                                                    maxcolwidths=[max_dt, max_bytes, new_max_path],
                                                    stralign='left',
                                                    tablefmt='plain')
                    print(table_1)
                    n_table += 1
                    try:
                        input()
                    except KeyboardInterrupt:
                        break

        if interact is False:
            table_1 = []
            if _mtime_scan is False:
                # 4 column table
                max_column_width = cli_character_limits.column_width_from_shutil(n=4)
                max_column_width_tot = max_column_width * 4
                max_dt = handler_post_process.longest_item(_results, idx=0)
                max_bytes = handler_post_process.longest_item(_results, idx=2)
                new_max_path = max_column_width_tot - max_dt - max_column_width - max_bytes - 8
                table_1 = tabulate.tabulate(_results,
                                            colalign=('left', 'right', 'right', 'left'),
                                            maxcolwidths=[max_dt, max_column_width, max_bytes, new_max_path],
                                            headers=('[Modified]', f'[Buffer: {_header_0.replace(": " + _query, "")}]',
                                                     '[Bytes]', f'[Files: {len(_results)}    Errors: {len(_exc)}]'),
                                            stralign='left')
            elif _mtime_scan is True:
                # 3 column table
                max_column_width = cli_character_limits.column_width_from_shutil(n=3)
                max_column_width_tot = max_column_width * 3
                max_dt = handler_post_process.longest_item(_results, idx=0)
                max_bytes = handler_post_process.longest_item(_results, idx=1)
                new_max_path = max_column_width_tot - max_dt - max_bytes - 8
                table_1 = tabulate.tabulate(_results,
                                            colalign=('left', 'right', 'left'),
                                            maxcolwidths=[max_dt, max_bytes, new_max_path],
                                            headers=('[Modified]', '[Bytes]',
                                                     f'[Files: {len(_results)}    Errors: {len(_exc)}]'),
                                            stralign='left')
            print(table_1)

    else:
        handler_print.display_zero_results(_results, _t_completion, _exc, _header_0)


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _p_scan: bool, _dt: str, _exc: list, _reveal_scan: bool,
                      _t_completion: str, _extract: bool, _verbose: bool,
                      interact: bool, _contents_scan: bool, _query: str, write_bool: bool, _mtime_scan: bool,
                      _bench: bool, _human_size=False):

    if _verbose is True:
        print('')
        print('-- formulating tabulated results...')
        print('')
    header_0 = 'Results'
    if _de_scan_bool is True:
        header_0 = 'De-Scan'
    elif _type_scan_bool is True:
        header_0 = 'Type Scan'
    elif _p_scan is True:
        header_0 = 'Password Protected Scan'
    elif _reveal_scan is True:
        header_0 = 'Reveal Scan'
    elif _contents_scan is True:
        header_0 = 'Contents Scan: ' + _query
    elif _mtime_scan is True:
        header_0 = 'Modified Time Scan'

    if _results is not None:
        if len(_results) >= 1:
            if len(_results[0]) >= 1:
                if _learn_bool is True:
                    learn_result_handler_display(_results=_results,
                                                 _exc=_exc,
                                                 _t_completion=_t_completion,
                                                 _verbose=_verbose)
                    asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
                    asyncio.run(handler_file.clean_database(fname=_db_recognized_files))

                else:
                    result_handler_display(_results=_results,
                                           _exc=_exc,
                                           _t_completion=_t_completion,
                                           _verbose=_verbose,
                                           _de_scan_bool=_de_scan_bool,
                                           _type_scan_bool=_type_scan_bool,
                                           _p_scan=_p_scan,
                                           _reveal_scan=_reveal_scan,
                                           _dt=_dt,
                                           _header_0=header_0,
                                           interact=interact,
                                           _contents_scan=_contents_scan,
                                           _query=_query,
                                           write_bool=write_bool,
                                           _mtime_scan=_mtime_scan,
                                           _bench=_bench,
                                           _human_size=_human_size)
            else:
                if _verbose is True:
                    handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
        else:
            if _verbose is True:
                handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
    else:
        if _verbose is True:
            handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
