""" Written by Benjamin Jack Cullen """

import asyncio
import handler_file
import handler_print
import tabulate
import cli_character_limits
import tabulate_helper
import power_time


# todo: optional write results


def learn_result_handler_display(_results: list, _exc: list, _t_completion: str, _pre_scan_time: str, _verbose: bool):

    max_column_width = cli_character_limits.column_width_from_screen_size_using_ratio(n=3)
    scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
    print(tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                            maxcolwidths=[max_column_width, max_column_width, max_column_width],
                            headers=('Learned                   ', 'Errors                ', 'Time                  '),
                            stralign='right'))


def result_handler_display(_results: list, _exc: list, _t_completion: str, _pre_scan_time: str, _verbose: bool,
                           _de_scan_bool: bool, _type_scan_bool: bool, _p_scan: bool,
                           _reveal_scan: bool, _dt: str, _header_0: str,
                           interact: bool):
    if len(_results) >= 1:
        tables = []
        max_column_width = cli_character_limits.column_width_from_screen_size_using_ratio(n=3)
        scan_time_human = power_time.convert_seconds_to_hours_minutes_seconds_time_delta(float(_t_completion))
        if _verbose is True:
            # verbose table: timings and things
            table_0 = tabulate.tabulate([[*[len(_results)], *[len(_exc)], *[scan_time_human]]],
                                        maxcolwidths=[max_column_width, max_column_width, max_column_width],
                                        headers=(f'{_header_0}', 'Errors                ', 'Time                  '),
                                        stralign='right')
            print(table_0)
            tables.append(table_0)
            print('')
            print('')

        # results table
        max_column_width = cli_character_limits.column_width_from_screen_size_using_ratio(n=3)
        table_1 = tabulate.tabulate(_results,
                                    colalign=('left', 'right', 'right', 'left'),
                                    maxcolwidths=[max_column_width, max_column_width, max_column_width, max_column_width],
                                    headers=('Modified', 'Buffer', 'Bytes', f'Files: {len(_results)}    Errors: {len(_exc)}'),
                                    stralign='left')
        tables.append(table_1)

        # filename
        part_fname = 'scan_results_'
        if _de_scan_bool is True:
            part_fname = 'de_scan'
        elif _type_scan_bool is True:
            part_fname = 'type_scan'
        elif _p_scan is True:
            part_fname = 'pscan'
        elif _reveal_scan is True:
            part_fname = 'reveal_scan'

        # write results
        for table in tables:
            asyncio.run(handler_file.write_scan_results(table, file=part_fname + '_' + _dt + '.txt', _dt=_dt))

        if interact is True:
            tabulate_helper.display_rows_interactively(max_limit=75,
                                                       results=_results,
                                                       table=table_1,
                                                       extra_input=False,
                                                       message='\n--- more ---\n',
                                                       function=None)
        else:
            print(table_1)

    else:
        handler_print.display_zero_results(_results, _t_completion, _exc, _header_0)


def result_handler_extract_method_0(_results: list, _exc: list, _t_completion: str, _pre_scan_time: str,
                                    _verbose: bool, _de_scan_bool: bool,
                                    _type_scan_bool: bool, _p_scan: bool, _reveal_scan: bool, _dt: str, _header_0: str,
                                    interact: bool):
    _sub_results = []
    for result in _results:
        for sub_result in result:
            _sub_results.append(sub_result)

    result_handler_display(_results=_sub_results,
                           _exc=_exc,
                           _t_completion=_t_completion,
                           _pre_scan_time=_pre_scan_time,
                           _verbose=_verbose,
                           _de_scan_bool=_de_scan_bool,
                           _type_scan_bool=_type_scan_bool,
                           _p_scan=_p_scan,
                           _reveal_scan=_reveal_scan,
                           _dt=_dt,
                           _header_0=_header_0,
                           interact=interact)


def result_handler_extract_method_1(_results: list, _exc: list, _t_completion: str, _pre_scan_time: str,
                                    _verbose: bool, _de_scan_bool: bool,
                                    _type_scan_bool: bool, _p_scan: bool, _reveal_scan: bool, _dt: str, _header_0: str,
                                    interact: bool):

    _sub_results = []
    for result in _results:
        concat_sub = []
        for sub_result in result:
            if isinstance(sub_result, list):
                _sub_results.append(sub_result)
            else:
                concat_sub.append(sub_result)
                if len(concat_sub) == 2:
                    _sub_results.append(concat_sub)

    result_handler_display(_results=_sub_results,
                           _exc=_exc,
                           _t_completion=_t_completion,
                           _pre_scan_time=_pre_scan_time,
                           _verbose=_verbose,
                           _de_scan_bool=_de_scan_bool,
                           _type_scan_bool=_type_scan_bool,
                           _p_scan=_p_scan,
                           _reveal_scan=_reveal_scan,
                           _dt=_dt,
                           _header_0=_header_0,
                           interact=interact)


def result_handler_de_scan(_results: list, _extract: bool, _exc: list, _t_completion: str, _pre_scan_time: str,
                           _verbose: bool, _de_scan_bool: bool,
                           _type_scan_bool: bool, _p_scan: bool, _reveal_scan: bool, _dt: str, _header_0: str,
                           interact: bool):
    if _extract is False:
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
                               _header_0=_header_0,
                               interact=interact)
    elif _extract is True:
        result_handler_extract_method_0(_results=_results,
                                        _exc=_exc,
                                        _t_completion=_t_completion,
                                        _pre_scan_time=_pre_scan_time,
                                        _verbose=_verbose,
                                        _de_scan_bool=_de_scan_bool,
                                        _type_scan_bool=_type_scan_bool,
                                        _p_scan=_p_scan,
                                        _reveal_scan=_reveal_scan,
                                        _dt=_dt,
                                        _header_0=_header_0,
                                        interact=interact)


def result_handler_type_scan(_results: list, _extract: bool, _exc: list, _t_completion: str, _pre_scan_time: str,
                             _verbose: bool, _de_scan_bool: bool,
                             _type_scan_bool: bool, _p_scan: bool, _reveal_scan: bool, _dt: str, _header_0: str,
                             interact: bool):
    # print(_results)
    if _extract is False:
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
                               _header_0=_header_0,
                               interact=interact)

    elif _extract is True:
        result_handler_extract_method_0(_results=_results,
                                        _exc=_exc,
                                        _t_completion=_t_completion,
                                        _pre_scan_time=_pre_scan_time,
                                        _verbose=_verbose,
                                        _de_scan_bool=_de_scan_bool,
                                        _type_scan_bool=_type_scan_bool,
                                        _p_scan=_p_scan,
                                        _reveal_scan=_reveal_scan,
                                        _dt=_dt,
                                        _header_0=_header_0,
                                        interact=interact)


def result_handler_p_scan(_results: list, _extract: bool, _exc: list, _t_completion: str, _pre_scan_time: str,
                          _verbose: bool, _de_scan_bool: bool,
                          _type_scan_bool: bool, _p_scan: bool, _reveal_scan: bool, _dt: str, _header_0: str,
                          interact: bool):
    if _extract is False:
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
                               _header_0=_header_0,
                               interact=interact)


def result_handler_reveal_scan(_results: list, _extract: bool, _exc: list, _t_completion: str, _pre_scan_time: str,
                               _verbose: bool, _de_scan_bool: bool,
                               _type_scan_bool: bool, _p_scan: bool, _reveal_scan: bool, _dt: str, _header_0: str,
                               interact: bool):
    if _extract is False:
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
                               _header_0=_header_0,
                               interact=interact)
    elif _extract is True:
        result_handler_extract_method_1(_results=_results,
                                        _exc=_exc,
                                        _t_completion=_t_completion,
                                        _pre_scan_time=_pre_scan_time,
                                        _verbose=_verbose,
                                        _de_scan_bool=_de_scan_bool,
                                        _type_scan_bool=_type_scan_bool,
                                        _p_scan=_p_scan,
                                        _reveal_scan=_reveal_scan,
                                        _dt=_dt,
                                        _header_0=_header_0,
                                        interact=interact)


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _p_scan: bool, _dt: str, _exc: list, _reveal_scan: bool,
                      _t_completion: str, _extract: bool, _verbose: bool, _pre_scan_time: str,
                      interact: bool):
    header_0 = 'Results'
    if _de_scan_bool is True:
        header_0 = 'De-Obfuscated/Unrecognized'
    elif _type_scan_bool is True:
        header_0 = 'Files of Type Specified   '
    elif _p_scan is True:
        header_0 = 'Password Protected        '
    elif _reveal_scan is True:
        header_0 = 'Files Revealed            '
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

                elif _de_scan_bool is True:
                    result_handler_de_scan(_results=_results,
                                           _extract=_extract,
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
                                           interact=interact)
                elif _type_scan_bool is True:
                    result_handler_type_scan(_results=_results,
                                             _extract=_extract,
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
                                             interact=interact)

                elif _p_scan is True:
                    result_handler_p_scan(_results=_results,
                                          _extract=_extract,
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
                                          interact=interact)

                elif _reveal_scan is True:
                    result_handler_reveal_scan(_results=_results,
                                               _extract=_extract,
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
                                               interact=interact)
            else:
                handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
        else:
            handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
    else:
        handler_print.display_zero_results(_results, _t_completion, _exc, header_0)
