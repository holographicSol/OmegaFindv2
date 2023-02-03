""" Written by Benjamin Jack Cullen """
import handler_chunk


def exception_format(e: Exception) -> list:
    e = str(e)
    return [e]


def separate_exception(_list: list) -> tuple:
    e = []
    new_l = []
    for item in _list:
        # errors
        found_error = False
        if len(item) > 0:
            if len(item) > 0:
                if item[0][0] == '[ERROR]':
                    for x in item:
                        if x not in e:
                            e.append(item)
                    found_error = True
        # results
        if found_error is False:
            new_l.append(item)
    e = handler_chunk.un_chunk_data(e, depth=1)
    return e, new_l
