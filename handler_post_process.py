""" Written by Benjamin Jack Cullen """

import handler_chunk


def results_filter(_list: list) -> tuple:
    log_filter = ['[ERROR]', '[INCOMPATIBLE NON-VARIANT]', '[INCOMPATIBLE VARIANT]', 'Password required']
    e = []
    new_l = []
    for item in _list:

        # errors
        found_error = False
        if isinstance(item, list):
            if len(item) > 0:
                if item[0] in log_filter:
                    e.append(item)
                    found_error = True
                else:
                    if len(item) > 0:
                        if not isinstance(item[0], int):
                            if item[0][0] in log_filter:
                                for x in item:
                                    if x not in e:
                                        e.append(item)
                                found_error = True
        # results
        if found_error is False:
            if item:
                new_l.append(item)
    e = handler_chunk.un_chunk_data(e, depth=1)
    return e, new_l


def longest_item(_list: list, idx: int) -> int:
    i_longest = 0
    for item in _list:
        try:
            if len(str(item[idx])) >= i_longest:
                i_longest = len(str(item[idx]))
        except Exception as e:
            print(item, e)
            pass
    return i_longest
