""" Written by Benjamin Jack Cullen """
import os
import subprocess
import screeninfo


def column_width_from_screen_size_using_ratio(n: int, reduce=0, add=0) -> int:
    """ return an integer predicated upon current screen resolution and column n (uses ratio 0.134 per 1px for
    font size 12).
    -> does not account for font size, etc.
    """
    if n == 0:
        n = 1

    w = 64
    for m in screeninfo.get_monitors():
        if m.is_primary is True:
            w = m.width
    w = int(int(w * 0.134) / n)  # currently using hardcoded ratio which could be variably set using font size.
    w -= reduce
    w += add
    return w


def column_width_from_screen_size_using_os_get_terminal_size(n: int, reduce=0, add=0) -> int:
    if n == 0:
        n = 1

    t_size = os.get_terminal_size().columns
    w = int(int(t_size) / n)  # divide size by column N
    w -= reduce
    w += add
    return w


def column_width_from_screen_size_using_tput(n: int, reduce=0, add=0) -> int:
    if n == 0:
        n = 1

    tput = subprocess.Popen(['tput', 'cols'], stdout=subprocess.PIPE)
    max_chars = int(tput.communicate()[0].strip())
    w = int(int(max_chars) / n)  # divide size by column N
    w -= reduce
    w += add
    return w
