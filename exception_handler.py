

def exception_format(e: Exception) -> list:
    e = str(e)
    e = e.split(': ')
    e1 = e[0]
    e2 = e[1].replace('\\\\', '\\')
    e2 = e2.replace("'", "")
    return [e1.strip(), e2.strip()]


def separate_exception(l: list):
    e = []
    new_l = []
    for item in l:
        if str(item[0]).startswith('[Errno '):
            e.append(item)
        else:
            new_l.append(item)
    return e, new_l
