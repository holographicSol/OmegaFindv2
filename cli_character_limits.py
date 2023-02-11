""" Written by Benjamin Jack Cullen """

import tabulate
import screeninfo


def column_width_from_screen_size_using_ratio(n: int) -> int:
    # print(f'n: {n}')
    w = 0
    for m in screeninfo.get_monitors():
        if m.is_primary is True:
            w = m.width
            # print(f'w: {w}')

    # print(f'suggested column width: {int(0.058*int(w) / int(n))}')
    return int(0.058*int(w) / int(n))


