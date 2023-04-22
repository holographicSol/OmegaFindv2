""" Written by Benjamin Jack Cullen """


def chunk_data(data: list, chunk_size: int) -> list:
    _chunks = [data[x:x + chunk_size] for x in range(0, len(data), chunk_size)]
    data = []
    for _chunk in _chunks:
        data.append(_chunk)
    return data


def un_chunk_data(data: list, depth: int) -> list:
    # with large amounts of data this can take a moment to complete. todo: re-work this for performance.
    new_data = data
    for i in range(0, depth):
        new_sub_data = []
        for dat in new_data:
            if dat is not None:
                for x in dat:
                    if x is not None:
                        if x not in new_sub_data:
                            new_sub_data.append(x)
        new_data = new_sub_data
    return new_data


def un_chunk_data_0(data: list) -> list:
    # good but slow with a huge list
    new_data = []
    for zero in data:
        for one in zero:
            if one not in new_data and one is not None:
                new_data.append(one)
    return new_data


def un_chunk_data_1(data: list) -> list:
    new_data = []
    for zero in data:
        for one in zero:
            for two in one:
                if two not in new_data and two is not None:
                    new_data.append(two)
    return new_data
