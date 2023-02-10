""" Written by Benjamin Jack Cullen """
import handler_strings


async def scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    buffer = handler_strings.sub_str(_buffer=buffer)
    if [suffix, buffer] not in _recognized_files:
        return [file, suffix, buffer]
