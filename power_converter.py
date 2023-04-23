""" Written by Benjamin Jack Cullen
"""
import binascii


def convert_to_ascii(*args: bytes) -> list:
    """ accepts *unpacked list """
    return [binascii.b2a_uu(arg) for arg in args]


def convert_bits_to_bytes(*args, byteorder: str) -> list:
    """ accepts *unpacked list, byteorder='big', byteorder='little'
    example: convert_bits_to_bytes(*[int("0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100", 2)], byteorder='big')
    """
    return [arg.to_bytes(((arg.bit_length() + 7) // 8), byteorder).decode() for arg in args]


def convert_bytes_to_bits(*args, byteorder: str) -> list:
    """ accepts *unpacked list, byteorder='big', byteorder='little'
    example: convert_bytes_to_bits(*['hello world'], byteorder='big'
    """
    return [bin(int.from_bytes(str(arg).encode(), byteorder)).replace('b', '') for arg in args]


def convert_bytes(*args, abbr: True) -> list:
    """ accepts *unpacked list """
    v = []
    ab_name = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB', 'GPB']
    full_name = ['bytes', 'Kilobytes', 'Megabytes', 'Gigabytes', 'Terabytes', 'Petabytes', 'Exabytes',
                 'Zettabytes', 'Yottabytes', 'Brontobytes', 'Geopbytes']
    for arg in args:
        for x in ab_name:
            if arg < 1024.0:
                if abbr is True:
                    v.append("%3.1f %s" % (arg, x))
                    break
                elif abbr is False:
                    v.append("%3.1f %s" % (arg, full_name[ab_name.index(x)]))
                    break
            arg /= 1024.0
    return v
