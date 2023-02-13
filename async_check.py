""" Written by Benjamin Jack Cullen """
import handler_strings
import asyncio
import handler_file


async def scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    buffer = handler_strings.sub_str(_buffer=buffer)
    if [suffix, buffer] not in _recognized_files:
        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file)
        return [m, buffer, s, file]


async def type_scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list) -> list:
    buffer = handler_strings.sub_str(_buffer=buffer)
    if [buffer] in _recognized_files:
        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file)
        return [m, buffer, s, file]
