from datetime import datetime
import re
import random
import string


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def randStr(chars=string.ascii_uppercase + string.digits, n=32) -> str:
    return ''.join(random.choice(chars) for _ in range(n))


def sub_str(_buffer: bytes) -> str:
    digi_str = r'[0-9]'
    return re.sub(digi_str, '', str(_buffer))
