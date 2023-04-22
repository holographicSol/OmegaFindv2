""" Written by Benjamin Jack Cullen """

import asyncio
import handler_file
import handler_post_process
import handler_print
import tabulate
import cli_character_limits
import tabulate_helper
import power_time
import time

# todo: optional write results + table_to_file: no max columns (considering parsing), print_table: max columns(readable)


def learn_result_handler_display(_results: list, _exc: list, _t_completion: str, _pre_scan_time: str, _verbose: bool):
    max_column_width = cli_character_limits.column_width_from_shutil(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
    print(tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                            maxcolwidths=[max_column_width, max_column_width, max_column_width],
                            headers=('Learned                   ', 'Errors                ', 'Time                  '),
                            stralign='right'))


def result_handler_display(_results: list, _exc: list, _t_completion: str, _pre_scan_time: str, _verbose: bool,
                           _de_scan_bool: bool, _type_scan_bool: bool, _p_scan: bool,
                           _reveal_scan: bool, _dt: str, _header_0: str,
                           interact: bool, _contents_scan: bool, write_bool: bool, _mtime_scan: bool,
                           _bench: bool, _query=''):
    if len(_results) >= 1:
        if _bench is True:
            t0 = time.perf_counter()
        tables = []
        max_column_width = cli_character_limits.column_width_from_shutil(n=3)
        scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
        if _verbose is True:
            # verbose table: timings and things
            table_0 = tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                                        maxcolwidths=[max_column_width, max_column_width, max_column_width],
                                        headers=(f'{_header_0}', 'Errors                ', 'Time                  '),
                                        stralign='right')
            print('')
            print(table_0)
            print('')

        # create results table
        if _mtime_scan is False:
            table_1 = tabulate.tabulate(_results,
                                        colalign=('left', 'right', 'right', 'left'),
                                        headers=('Modified', f'Buffer [{_header_0}]', 'Bytes', f'Files: {len(_results)}    Errors: {len(_exc)}'),
                                        stralign='left')
            tables.append(table_1)
        elif _mtime_scan is True:
            table_1 = tabulate.tabulate(_results,
                                        colalign=('left', 'right', 'left'),
                                        headers=('Modified', 'Bytes', f'Files: {len(_results)}    Errors: {len(_exc)}'),
                                        stralign='left')
            tables.append(table_1)

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

        # write results
        if write_bool is True:
            for table in tables:
                asyncio.run(handler_file.write_scan_results(table, file=part_fname + '_' + _dt + '.txt', _dt=_dt))

        # enumeration for reasonable column widths
        if _mtime_scan is False:
            max_column_width = cli_character_limits.column_width_from_shutil(n=4)
            max_column_width_tot = max_column_width * 4
            max_dt = handler_post_process.longest_item(_results, idx=0)
            max_bytes = handler_post_process.longest_item(_results, idx=2)
            new_max_path = max_column_width_tot - max_dt - max_column_width - max_bytes - 8
            table_1 = tabulate.tabulate(_results,
                                        colalign=('left', 'right', 'right', 'left'),
                                        maxcolwidths=[max_dt, max_column_width, max_bytes, new_max_path],
                                        headers=('[Modified]', f'[Buffer: {_header_0.replace(": "+_query, "")}]', '[Bytes]', f'[Files: {len(_results)}    Errors: {len(_exc)}]'),
                                        stralign='left')
        elif _mtime_scan is True:
            max_column_width = cli_character_limits.column_width_from_shutil(n=3)
            max_column_width_tot = max_column_width * 3
            max_dt = handler_post_process.longest_item(_results, idx=0)
            max_bytes = handler_post_process.longest_item(_results, idx=1)
            new_max_path = max_column_width_tot - max_dt - max_bytes - 8
            table_1 = tabulate.tabulate(_results,
                                        colalign=('left', 'right', 'left'),
                                        maxcolwidths=[max_dt, max_bytes, new_max_path],
                                        headers=('[Modified]', '[Bytes]', f'[Files: {len(_results)}    Errors: {len(_exc)}]'),
                                        stralign='left')

        if _bench is True:
            print(f'tabulation time: {time.perf_counter() - t0}')
            print('')

        # display results tale
        if interact is True:
            tabulate_helper.display_rows_interactively(max_limit=75,
                                                       results=_results,
                                                       table=table_1,
                                                       extra_input=False,
                                                       message='\n-- more --\n',
                                                       function=None)
        else:
            print(table_1)

    else:
        handler_print.display_zero_results(_results, _t_completion, _exc, _header_0)


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _p_scan: bool, _dt: str, _exc: list, _reveal_scan: bool,
                      _t_completion: str, _extract: bool, _verbose: bool, _pre_scan_time: str,
                      interact: bool, _contents_scan: bool, _query: str, write_bool: bool, _mtime_scan: bool,
                      _bench: bool):

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
                                                 _pre_scan_time=_pre_scan_time,
                                                 _verbose=_verbose)
                    asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
                    asyncio.run(handler_file.clean_database(fname=_db_recognized_files))

                else:
                    result_handler_display(_results=_results,
                                           _exc=_exc,
                                           _t_completion=_t_completion,
                                           _pre_scan_time=_pre_scan_time,
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
                                           _bench=_bench)
            else:
                if _verbose is True:
                    handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
        else:
            if _verbose is True:
                handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
    else:
        if _verbose is True:
            handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
