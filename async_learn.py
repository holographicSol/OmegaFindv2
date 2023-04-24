""" Written by Benjamin Jack Cullen """

import asyncio
import handler_file

x_learn = []


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    return [await scan_learn(item, _recognized_files, _buffer_max) for item in chunk]


async def scan_learn_check(suffix: str, buffer: bytes, _recognized_files: list) -> list:
    global x_learn
    if [suffix, buffer] not in x_learn:
        x_learn.append([suffix, buffer])
        if [suffix, buffer] not in _recognized_files:
            return [suffix, buffer]


async def scan_learn(file: str, _recognized_files: list, _buffer_max: int) -> list:
    try:
        # todo
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await scan_learn_check(suffix, buffer, _recognized_files)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result
