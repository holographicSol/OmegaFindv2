""" Written by Benjamin Jack Cullen """

import handler_strings
import asyncio
import handler_file


async def scan_check(_file: str, _suffix: str, _buffer: bytes, _recognized_files: list, _digits=True,
                     _human_size=False) -> list:
    sub_buffer = _buffer
    if _digits is False:
        sub_buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=_buffer)
    if [_suffix, sub_buffer] not in _recognized_files:
        # todo
        m = await asyncio.to_thread(handler_file.get_m_time, _file)
        s = await asyncio.to_thread(handler_file.get_size, _file, _human_size)
        return [m, _buffer, s, _file]


async def type_scan_check(_file: str, _buffer: bytes, _recognized_files: list, _digits=True,
                          _human_size=False) -> list:
    sub_buffer = _buffer
    if _digits is False:
        sub_buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=_buffer)
    if [sub_buffer] in _recognized_files:
        # todo
        m = await asyncio.to_thread(handler_file.get_m_time, _file)
        s = await asyncio.to_thread(handler_file.get_size, _file, _human_size)
        return [m, _buffer, s, _file]
