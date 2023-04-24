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
