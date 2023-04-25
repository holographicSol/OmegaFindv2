
def sort_len_3(data: list, sort_mode: str, _verbose: bool):
    try:
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
    except TypeError:
        if _verbose is True:
            for x in data:
                if not isinstance(x[0], str):
                    print(f'Not String ({x[0]}): {x}')
                if not isinstance(x[1], str):
                    print(f'Not String ({x[1]}): {x}')
                if not isinstance(x[2], str):
                    print(f'Not String ({x[2]}): {x}')
                if not isinstance(x[3], str):
                    print(f'Not String ({x[3]}): {x}')

    return data


def sort_len_2(data: list, sort_mode: str, _verbose: bool):
    try:
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
    except TypeError:
        if _verbose is True:
            for x in data:
                if not isinstance(x[0], str):
                    print(f'Not String ({x[0]}): {x}')
                if not isinstance(x[1], str):
                    print(f'Not String ({x[1]}): {x}')
                if not isinstance(x[2], str):
                    print(f'Not String ({x[2]}): {x}')
    return data
