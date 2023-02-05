import asyncio
import handler_file


def result_handler(_results: list, msg: str):
    print(f'\n   {msg}')
    i_result = 0
    for result in _results:
        if i_result <= 3:
            print('  ', result)
            i_result += 1
        else:
            print('-- more results available in scan results file(s).')
            break


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _p_scan: bool, _dt: str, _exc: list):
    if _results is not None:
        if len(_results) >= 1:
            if _learn_bool is True:
                print(f'-- new definitions {len(_results)}')
                print('-- updating definitions ..')
                asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
                asyncio.run(handler_file.clean_database(fname=_db_recognized_files))
            elif _de_scan_bool is True:
                print(f'-- found {len(_results)} unrecognized or obfuscated files (errors: {len(_exc)}).')
                # print('-- writing results ..')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_de-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler(_results=_results, msg='[Unrecognized]')
            elif _type_scan_bool is True:
                print(f'-- found {len(_results)} files (errors: {len(_exc)}).')
                # print('-- writing results ..')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_type-scan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler(_results=_results, msg='[Found]')
            elif _p_scan is True:
                print(f'-- found {len(_results)} password protected files (errors: {len(_exc)}).')
                # print('-- writing results ..')
                asyncio.run(handler_file.write_scan_results(*_results,
                                                            file='scan_results_pscan_' + _dt + '.txt',
                                                            _dt=_dt))
                result_handler(_results=_results, msg='[PASSWORD PROTECTED]')
        else:
            print('-- zero results.')
    else:
        print('-- zero results.')
    print('')
    print('')
