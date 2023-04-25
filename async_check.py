""" Written by Benjamin Jack Cullen """

import handler_strings
import asyncio
import handler_file


async def check_in_list(_list_1: list, _list_2: list) -> bool:
    if _list_1 not in _list_2:
        return False


async def check_not_in_list(_list_1: list, _list_2: list) -> bool:
    if _list_1 not in _list_2:
        return False


async def scan_check(_file: str, _suffix: str, _buffer: bytes, _recognized_files: list, _digits=True,
                     _human_size=False) -> list:
    sub_buffer = _buffer
    if _digits is False:
        sub_buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=_buffer)
    assoc = [_suffix, _buffer]
    if await check_in_list(_list_1=assoc, _list_2=sub_buffer) is False:
        m = await asyncio.to_thread(handler_file.get_m_time, _file=_file)
        s = await asyncio.to_thread(handler_file.get_size, _file)
        return [m, _buffer, s, _file]


async def type_scan_check(_file: str, _buffer: bytes, _recognized_files: list, _digits=True,
                          _human_size=False) -> list:
    sub_buffer = _buffer
    if _digits is False:
        sub_buffer = await asyncio.to_thread(handler_strings.sub_str, _buffer=_buffer)
    assoc = [sub_buffer]
    if await check_not_in_list(_list_1=assoc, _list_2=sub_buffer) is False:
        m = await asyncio.to_thread(handler_file.get_m_time, _file=_file)
        s = await asyncio.to_thread(handler_file.get_size, _file=_file)
        return [m, _buffer, s, _file]
