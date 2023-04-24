""" Written by Benjamin Jack Cullen """

import string


def valid_alphanum(chars: str):
    _valid_alphanum = string.ascii_uppercase + string.ascii_lowercase + string.digits + '.' + '_' + '-'
    bool_valid_chars = True
    for char in chars:
        if char not in _valid_alphanum:
            bool_valid_chars = False
            print('invalid character(s): characters must be alphanumeric.')
            break
    return bool_valid_chars


def input_singularity(message='', condition=''):
    """ This function tries to reduce input from all over the program into this single point for
      ease of sanitization etc. """

    try:
        x_input = input(message)
    except KeyboardInterrupt:
        exit(0)

    if not condition:
        return x_input

    elif condition == 'alphanum':
        if valid_alphanum(chars=x_input) is True:
            return x_input
