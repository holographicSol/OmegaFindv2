

def exception_format(e: Exception) -> list:
    e = str(e)
    return [e]


def separate_exception(_list: list) -> tuple:
    e = []
    new_l = []
    for item in _list:
        if str(item[0]).startswith('[Errno '):
            e.append(item)
        else:
            new_l.append(item)
    return e, new_l
