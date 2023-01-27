import asyncio
import handler_file


def result_handler(_results: list):
    if len(_results) <= 12:
        print('[Unrecognized files]:')
        for result in _results:
            print(' ', result)
    else:
        print('[Unrecognized files]:')
        i_result = 0
        for result in _results:
            if i_result <= 12:
                print(' ', result)
                i_result += 1
            else:
                break


def post_scan_results(_results: list, _db_recognized_files: list,
                      _learn_bool: bool, _de_scan_bool: bool, _type_scan_bool: bool, _dt: str):
    if len(_results) >= 1:
        if _learn_bool is True:
            print(f'[New Definitions] {len(_results)}')
            print('[Updating Definitions] ..')
            asyncio.run(handler_file.write_definitions(*_results, file=_db_recognized_files))
            asyncio.run(handler_file.clean_database(fname=_db_recognized_files))
        elif _de_scan_bool is True:
            print(f'[Unrecognized Files] {len(_results)}')
            print('[Writing Scan Results] ..')
            asyncio.run(handler_file.write_scan_results(*_results, file='scan_results__' + _dt + '.txt', _dt=_dt))
            result_handler(_results=_results)
        elif _type_scan_bool is True:
            print(f'[Found Files] {len(_results)}')
            print('[Writing Scan Results] ..')
            asyncio.run(handler_file.write_scan_results(*_results, file='scan_results__' + _dt + '.txt', _dt=_dt))
    else:
        print('[Zero Results]')
    print('')
