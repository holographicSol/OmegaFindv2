import asyncio
import handler_file

# todo: press enter to show more results, q to quit


def result_handler_no_extract(_results: list):
    i_result = 0
    for result in _results:
        if i_result <= 500:
            print(result)
            i_result += 1
        else:
            print('-- more results available in scan results file(s).')
            break


def result_handler_de_scan(_results: list, msg: str, _extract: bool):
    print(f'\n{msg}')
    if _extract is False:
        result_handler_no_extract(_results=_results)
    elif _extract is True:
        i_result = 0
        for result in _results:
            if i_result <= 500:
                for sub_result in result:
                    if i_result <= 500:
                        print(sub_result)
                        i_result += 1
                    else:
                        break
            else:
                print('-- more results available in scan results file(s).')
                break


def result_handler_type_scan(_results: list, msg: str, _extract: bool):
    print(f'\n{msg}')
    if _extract is False:
        result_handler_no_extract(_results=_results)
    elif _extract is True:
        i_result = 0
        for result in _results:
            if i_result <= 500:
                for sub_result in result:
                    if i_result <= 500:
                        print(sub_result)
                        i_result += 1
                    else:
                        break
            else:
                print('-- more results available in scan results file(s).')
                break


def result_handler_p_scan(_results: list, msg: str, _extract: bool):
    print(f'\n{msg}')
    if _extract is False:
        result_handler_no_extract(_results=_results)


def result_handler_reveal_scan(_results: list, msg: str, _extract: bool):
    print(f'\n{msg}')
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
                            print(sub_result)
                        else:
                            concat_sub.append(sub_result)
                            if len(concat_sub) == 2:
                                print(concat_sub)
                        i_result += 1
                    else:
                        break
            else:
                print('-- more results available in scan results file(s).')
                break


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _p_scan: bool, _dt: str, _exc: list, _reveal_scan: bool,
                      _t_completion: str, _extract: bool):
    if _results is not None:
        if len(_results) >= 1:
            if _learn_bool is True:
                print(f'-- new definitions {len(_results)}')
                print('-- updating definitions ..')
                asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
                asyncio.run(handler_file.clean_database(fname=_db_recognized_files))
            elif _de_scan_bool is True:
                print(f'-- found {len(_results)} unrecognized or obfuscated files (errors: {len(_exc)}). time: {_t_completion}')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_de-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_de_scan(_results=_results, msg='[Unrecognized]', _extract=_extract)
            elif _type_scan_bool is True:
                print(f'-- found {len(_results)} files (errors: {len(_exc)}). time: {_t_completion}')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_type-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_type_scan(_results=_results, msg='[Found]', _extract=_extract)
            elif _p_scan is True:
                print(f'-- found {len(_results)} password protected files (errors: {len(_exc)}). time: {_t_completion}')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_pscan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_p_scan(_results=_results, msg='[PASSWORD PROTECTED]', _extract=_extract)
            elif _reveal_scan is True:
                print(f'-- found {len(_results)} files (errors: {len(_exc)}). time: {_t_completion}')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_reveal-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler_reveal_scan(_results=_results, msg='[Found]', _extract=_extract)
        else:
            print(f'-- zero results (errors: {len(_exc)}).')
    else:
        print(f'-- zero results (errors: {len(_exc)}).')
    print('')
    print('')
