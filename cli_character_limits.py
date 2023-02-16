""" Written by Benjamin Jack Cullen """
import os
import subprocess
import screeninfo


def column_width_from_screen_size_using_ratio(n: int, reduce=0, add=0, ratio=0.134) -> int:
    """ Default ratio defined for font size 12. """

    w = 64
    for m in screeninfo.get_monitors():
        if m.is_primary is True:
            w = m.width
    w = add_sub(n=int(int(w * ratio) / set_n(n)), reduce=reduce, add=add)
    return w


def column_width_from_screen_size_using_os_get_terminal_size(n: int, reduce=0, add=0) -> int:

    w = add_sub(n=int(int(os.get_terminal_size().columns) / set_n(n)), reduce=reduce, add=add)
    return w


def column_width_from_screen_size_using_tput(n: int, reduce=0, add=0) -> int:

    w = int(int(int(subprocess.Popen(['tput', 'cols'], stdout=subprocess.PIPE).communicate()[0].strip())) / set_n(n))
    w = add_sub(n=w, reduce=reduce, add=add)
    return w


def add_sub(n, reduce=0, add=0):
    n -= reduce
    n += add
    return n


def set_n(n):
    if n <= 0:
        n = 1
    return n
