""" Written by Benjamin Jack Cullen """

import os
from datetime import datetime
import re
import random
import string
import variable_strings
import handler_print
import asyncio
import handler_file
import unicodedata


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def randStr(chars=string.ascii_uppercase + string.digits, n=32) -> str:
    return ''.join(random.choice(chars) for _ in range(n))


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())


def sub_str(_buffer: bytes) -> str:
    return re.sub(variable_strings.digi_str, '', str(_buffer))


def input_open_dir(_list) -> bool:
    repeat_request = False
    if _list:
        usr_input = handler_print.input_select()
        if usr_input.isdigit():
            repeat_request = True
            usr_input = int(usr_input)
            result = _list[usr_input]
            idx = result[3].rfind('\\')
            fullpath = result[3][:idx]
            if usr_input <= len(_list):
                os.startfile(fullpath)
    return repeat_request


def input_select_report(_list):
    if _list:
        usr_input = handler_print.input_select()
        if usr_input.isdigit():
            usr_input = int(usr_input)
            result = _list[usr_input][1]
            asyncio.run(handler_file.read_report(fname=result))
