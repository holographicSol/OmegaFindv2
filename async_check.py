""" Written by Benjamin Jack Cullen """

import handler_strings
import asyncio
import handler_file


async def scan_check(file: str, suffix: str, buffer: bytes, _recognized_files: list, _digits=True,
                     human_size=False) -> list:
    sub_buffer = buffer
    if _digits is False:
        sub_buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=buffer)  # digitless
    if [suffix, sub_buffer] not in _recognized_files:
        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file, human_size)
        return [m, buffer, s, file]


async def type_scan_check(file: str, buffer: bytes, _recognized_files: list, _digits=True,
                          human_size=False) -> list:
    sub_buffer = buffer
    if _digits is False:
        sub_buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=buffer)  # digitless
    if [sub_buffer] in _recognized_files:
        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file, human_size)
        return [m, buffer, s, file]
