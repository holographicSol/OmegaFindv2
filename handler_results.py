import asyncio
import handler_file


def result_handler(_results: list):
    print('-- unrecognized files:')
    i_result = 0
    for result in _results:
        if i_result <= 12:
            print(' ', result)
            i_result += 1
        else:
            break


def post_scan_results(_results: list, _db_recognized_files: str, _learn_bool: bool, _de_scan_bool: bool,
                      _type_scan_bool: bool, _dt: str):
    if len(_results) >= 1:
        if _learn_bool is True:
            print(f'-- new definitions {len(_results)}')
            print('-- updating definitions ...')
            asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
            asyncio.run(handler_file.clean_database(fname=_db_recognized_files))
        elif _de_scan_bool is True:
            print(f'-- unrecognized files: {len(_results)}')
            print('-- writing results ...')
            asyncio.run(handler_file.write_scan_results(*_results,
                                                        file='scan_results__' + _dt + '.txt',
                                                        _dt=_dt))
            result_handler(_results=_results)
        elif _type_scan_bool is True:
            print(f'-- found files: {len(_results)}')
            print('-- writing results ...')
            asyncio.run(handler_file.write_scan_results(*_results,
                                                        file='scan_results__' + _dt + '.txt',
                                                        _dt=_dt))
            result_handler(_results=_results)
    else:
        print('-- zero results.')
    print('')
