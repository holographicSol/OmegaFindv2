""" Written by Benjamin Jack Cullen """


def chunk_data(data: list, chunk_size: int) -> list:
    _chunks = [data[x:x + chunk_size] for x in range(0, len(data), chunk_size)]
    data = []
    for _chunk in _chunks:
        data.append(_chunk)
    return data


def un_chunk_data(data: list, depth: int) -> list:
    new_data = data
    for i in range(0, depth):
        new_sub_data = []
        for dat in new_data:
            for x in dat:
                if x is not None:
                    if x not in new_sub_data:
                        new_sub_data.append(x)
        new_data = new_sub_data
    return new_data


def sub_int_sort(_list: list) -> list:
    return sorted(_list, key=lambda x: x[0])


def rem_tags(_list: list) -> list:
    for x in _list:
        x.remove(x[0])
    return _list
