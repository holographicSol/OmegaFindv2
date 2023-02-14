""" Written by Benjamin Jack Cullen """

import screeninfo


def column_width_from_screen_size_using_ratio(n: int, reduce=0, add=0) -> int:
    """ return an integer predicated upon current screen resolution and column n (uses ratio 0.116 per 1px).
    -> does not account for font size, etc.
    """
    if n == 0:
        n = 1

    w = 0
    for m in screeninfo.get_monitors():
        if m.is_primary is True:
            w = m.width
    w = int(int(w * 0.150) / n)  # currently using hardcoded ratio which could be variably set using font size.
    w -= reduce
    w += add
    return w
