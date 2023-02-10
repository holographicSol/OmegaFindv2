import handler_strings


async def check_extract(_extract: bool, _buffer: bytes) -> bool:
    if _extract is True:
        _buffer = str(_buffer).strip()
        return True


async def scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    buffer = handler_strings.sub_str(_buffer=buffer)
    if [suffix, buffer] not in _recognized_files:
        return [file, suffix, buffer]
