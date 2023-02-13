
def pscan(_list: list) -> list:
    new = []
    for item in _list:
        for x in item:
            if x not in new:
                new.append(x)
    return new
