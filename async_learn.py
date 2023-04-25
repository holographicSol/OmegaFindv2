""" Written by Benjamin Jack Cullen """

import asyncio
import handler_file
import async_check

x_learn = []


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await scan_learn(_file=item,
                             _recognized_files=_recognized_files,
                             _buffer_max=_buffer_max) for item in chunk]


async def scan_learn_check(_suffix: str, _buffer: bytes, _recognized_files: list) -> list:
    global x_learn
    assoc = [_suffix, _buffer]
    if await async_check.check_list(_list_1=assoc, _list_2=x_learn) is False:
        x_learn.append(assoc)
        if await async_check.check_list(_list_1=assoc, _list_2=_recognized_files) is False:
            return assoc


async def scan_learn(_file: str, _recognized_files: list, _buffer_max: int) -> list:
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, _file=_file)
        _result = await scan_learn_check(_suffix=suffix, _buffer=buffer, _recognized_files=_recognized_files)
    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    return _result
