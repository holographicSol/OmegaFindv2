""" Written by Benjamin Jack Cullen """
import handler_chunk


def exception_format(e: Exception) -> list:
    e = str(e)
    return [e]


def results_filter(_list: list) -> tuple:
    log_filter = ['[ERROR]', '[INCOMPATIBLE NON-VARIANT]', '[INCOMPATIBLE VARIANT]']
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
