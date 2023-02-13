""" Written by Benjamin Jack Cullen """
import handler_chunk
import handler_file
import handler_strings
import asyncio


def typescan(_list: list, _recognized_files: list):
    # print('typescan', _list)
    return _list


def descan(_list: list, _recognized_files: list):
    new = []
    for item in _list:
        for x in item:
            if [x] not in new:
                new.append([x])
    return new


async def pscan(_list: list) -> list:
    new = []
    for item in _list:
        for x in item:
            if x not in new:
                new.append(x)
    return new


def results_filter(_list: list) -> tuple:
    log_filter = ['[ERROR]', '[INCOMPATIBLE NON-VARIANT]', '[INCOMPATIBLE VARIANT]', 'Password required']
    e = []
    new_l = []
    for item in _list:

        # errors
        found_error = False
        if len(item) > 0:
            if item[0] in log_filter:
                e.append(item)
                found_error = True
            else:
                if len(item) > 0:
                    # print('item:', item)
                    if not isinstance(item[0], int):
                        # print('item check 1:', item)
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
