import asyncio
import handler_strings
import handler_file
import async_check
import handler_extraction_method


async def entry_point_p_scan(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    return [await p_scan(item, _buffer_max, _extract=True, _target=_target, _program_root=_program_root) for item in chunk]


async def p_scan(file: str, _buffer_max: int, _extract: bool, _target: str, _program_root: str) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        if await async_check.check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_p_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max, _target=_target,
                                           _program_root=_program_root)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_p_scan(_buffer: bytes, _file: str, _buffer_max: int, _target: str, _program_root: str) -> list:
    _result = [_file]
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    _result_bool, _results = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                     file=_file,
                                                     temp_directory=_tmp,
                                                     _target=_target,
                                                     _static_tmp=_tmp)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    final_res = []
    for res in _results:
        if 'Password required' in res:
            if res not in final_res:
                final_res.append(res)
        elif res[0] == '[ERROR]':
            if res not in final_res:
                final_res.append(res)
    return final_res
