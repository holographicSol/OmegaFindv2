
def sort_len_3(data: list, sort_mode: str):
    if sort_mode == '--sort=mtime':
        data = sorted(data, key=lambda x: x[0])
    elif sort_mode == '--sort=buffer':
        data = sorted(data, key=lambda x: x[1])
    elif sort_mode == '--sort=size':
        data = sorted(data, key=lambda x: int(x[2]))
    elif sort_mode == '--sort=file':
        data = sorted(data, key=lambda x: x[3])

    elif sort_mode == '--sort-reverse=mtime':
        data = sorted(data, key=lambda x: x[0], reverse=True)
    elif sort_mode == '--sort-reverse=buffer':
        data = sorted(data, key=lambda x: x[1], reverse=True)
    elif sort_mode == '--sort-reverse=size':
        data = sorted(data, key=lambda x: int(x[2]), reverse=True)
    elif sort_mode == '--sort-reverse=file':
        data = sorted(data, key=lambda x: x[3], reverse=True)

    return data


def sort_len_2(data: list, sort_mode: str):
    if sort_mode == '--sort=mtime':
        data = sorted(data, key=lambda x: x[0])
    elif sort_mode == '--sort=size':
        data = sorted(data, key=lambda x: int(x[1]))
    elif sort_mode == '--sort=file':
        data = sorted(data, key=lambda x: x[2])

    elif sort_mode == '--sort-reverse=mtime':
        data = sorted(data, key=lambda x: x[0], reverse=True)
    elif sort_mode == '--sort-reverse=size':
        data = sorted(data, key=lambda x: int(x[1]), reverse=True)
    elif sort_mode == '--sort-reverse=file':
        data = sorted(data, key=lambda x: x[2], reverse=True)

    return data


def sort_len_2_string_match(data: list, sort_mode: str):
    if sort_mode == '--sort=mtime':
        data = sorted(data, key=lambda x: x[1])
    elif sort_mode == '--sort=size':
        data = sorted(data, key=lambda x: int(x[2]))
    elif sort_mode == '--sort=file':
        data = sorted(data, key=lambda x: x[3])

    elif sort_mode == '--sort-reverse=mtime':
        data = sorted(data, key=lambda x: x[1], reverse=True)
    elif sort_mode == '--sort-reverse=size':
        data = sorted(data, key=lambda x: int(x[2]), reverse=True)
    elif sort_mode == '--sort-reverse=file':
        data = sorted(data, key=lambda x: x[3], reverse=True)

    return data
