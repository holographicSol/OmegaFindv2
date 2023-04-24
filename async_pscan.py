""" Written by Benjamin Jack Cullen """

import asyncio
import handler_strings
import handler_file
import handler_extraction_method


async def entry_point_p_scan(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    human_size = kwargs.get('human_size')
    x = [await p_scan(item, _buffer_max, _extract=True, _target=_target, _program_root=_program_root,
                      human_size=human_size) for item in chunk]
    return x


async def p_scan(file: str, _buffer_max: int, _extract: bool, _target: str, _program_root: str,
                 human_size=False) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(_file=file, _buffer_max=_buffer_max)
        _result = await extract_p_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max, _target=_target,
                                       _program_root=_program_root, human_size=human_size)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_p_scan(_buffer: bytes, _file: str, _buffer_max: int, _target: str, _program_root: str,
                         human_size=False) -> list:
    _result = [_file]
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    _result_bool, _results = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                     file=_file,
                                                     temp_directory=_tmp,
                                                     _target=_target,
                                                     _static_tmp=_tmp)
    # todo
    final_result = await handler_file.stat_files(_results, _target, _tmp, human_size)

    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return final_result
