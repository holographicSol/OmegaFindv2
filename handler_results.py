""" Written by Benjamin Jack Cullen """
import asyncio
import handler_file
import handler_print
import tabulate
import cli_character_limits


# todo: press enter to show more results, q to quit


def result_handler_no_extract(_results: list):
    max_column_width = cli_character_limits.column_width_from_screen_size_using_ratio(n=len(_results))
    print(tabulate.tabulate(_results, tablefmt="simple", maxcolwidths=[max_column_width, max_column_width])) # 800x600 (inc. Windows Defaults)


def result_handler_de_scan(_results: list, _extract: bool):
    if _extract is False:
        result_handler_no_extract(_results=_results)
    elif _extract is True:
        i_result = 0
        for result in _results:
            if i_result <= 500:
                for sub_result in result:
                    if i_result <= 500:
                        handler_print.display_result(_item=sub_result)
                        i_result += 1
                    else:
                        break
            else:
                handler_print.display_more_results_available()
                break


def result_handler_type_scan(_results: list, _extract: bool):
    if _extract is False:
        result_handler_no_extract(_results=_results)
    elif _extract is True:
        i_result = 0
        for result in _results:
            if i_result <= 500:
                for sub_result in result:
                    if i_result <= 500:
                        handler_print.display_result(_item=sub_result)
                        i_result += 1
                    else:
                        break
            else:
                handler_print.display_more_results_available()
                break


def result_handler_p_scan(_results: list, _extract: bool):
    if _extract is False:
        result_handler_no_extract(_results=_results)


def result_handler_reveal_scan(_results: list, _extract: bool):
    if _extract is False:
        result_handler_no_extract(_results=_results)
    elif _extract is True:
        i_result = 0
        for result in _results:
            if i_result <= 500:
                concat_sub = []
                for sub_result in result:
                    if i_result <= 500:
                        if isinstance(sub_result, list):
                            handler_print.display_result(_item=sub_result)
                        else:
                            concat_sub.append(sub_result)
                            if len(concat_sub) == 2:
                                handler_print.display_result(_item=concat_sub)
                        i_result += 1
                    else:
                        break
            else:
                handler_print.display_more_results_available()
                break


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _p_scan: bool, _dt: str, _exc: list, _reveal_scan: bool,
                      _t_completion: str, _extract: bool, _verbose: bool):
    if _results is not None:
        if len(_results) >= 1:
            if _learn_bool is True:
                if _verbose is True:
                    handler_print.display_learning_results_overview(_results)
                asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
                asyncio.run(handler_file.clean_database(fname=_db_recognized_files))

            elif _de_scan_bool is True:
                if _verbose is True:
                    handler_print.display_de_scan_results_overview(_results, _exc, _t_completion)
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_de-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_de_scan(_results=_results, _extract=_extract)

            elif _type_scan_bool is True:
                if _verbose is True:
                    handler_print.display_type_scan_results_overview(_results, _exc, _t_completion)
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_type-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_type_scan(_results=_results, _extract=_extract)

            elif _p_scan is True:
                if _verbose is True:
                    handler_print.display_p_scan_results_overview(_results, _exc, _t_completion)
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_pscan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_p_scan(_results=_results, _extract=_extract)

            elif _reveal_scan is True:
                if _verbose is True:
                    handler_print.display_reveal_scan_results_overview(_results, _exc, _t_completion)
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_reveal-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_reveal_scan(_results=_results, _extract=_extract)

        else:
            handler_print.display_zero_results(_exc)
    else:
        handler_print.display_zero_results(_exc)
