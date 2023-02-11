""" Written by Benjamin Jack Cullen """

import tabulate
import screeninfo


def column_width_from_screen_size_using_ratio(n: int) -> int:
    w = 0
    for m in screeninfo.get_monitors():
        if m.is_primary is True:
            w = m.width
    return int(0.058*int(w))
