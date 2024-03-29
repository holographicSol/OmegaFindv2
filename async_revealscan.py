""" Written by Benjamin Jack Cullen """

import asyncio
import handler_strings
import handler_file
import scanfs
import handler_extraction_method


async def entry_point_reveal_scan(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    _extract = kwargs.get('extract')
    human_size = kwargs.get('human_size')

    if _extract is False:
        return [await reveal_scan(_file=item, _buffer_max=_buffer_max, _extract=_extract, _target=_target,
                                  _program_root=_program_root, _human_size=human_size) for item in chunk]
    elif _extract is True:
        return [await reveal_scan_extract(_file=item, _buffer_max=_buffer_max, _extract=_extract, _target=_target,
                                          _program_root=_program_root, _human_size=human_size) for item in chunk]


async def reveal_scan(_file: str, _buffer_max: int, _extract: bool, _target: str, _program_root: str,
                      _human_size=False) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        m = await asyncio.to_thread(handler_file.get_m_time, _file=_file)
        s = await asyncio.to_thread(handler_file.get_size, _file=_file)
        return [m, buffer, s, _file]

    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    return _result


async def reveal_scan_extract(_file: str, _buffer_max: int, _extract: bool, _target: str, _program_root: str,
                              _human_size=False) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        _result = await extract_reveal_scan(_file=_file, _buffer_max=_buffer_max, _target=_target,
                                            _program_root=_program_root, _buffer=buffer, _human_size=_human_size)
    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    return _result


async def extract_reveal_scan(_file: str, _buffer_max: int, _target: str, _program_root: str,
                              _buffer: bytes, _human_size=False) -> list:
    _results = []
    m = await asyncio.to_thread(handler_file.get_m_time, _file=_file)
    s = await asyncio.to_thread(handler_file.get_size, _file=_file)
    _results = [[m, _buffer, s, _file]]
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _path=_tmp)
        sub_files[:] = [item for sublist in sub_files for item in sublist]
        for sub_file in sub_files:
            buffer = await handler_file.async_read_bytes(_file=sub_file, _buffer_max=_buffer_max)
            m = await asyncio.to_thread(handler_file.get_m_time, _file=sub_file)
            s = await asyncio.to_thread(handler_file.get_size, _file=sub_file)
            res = [m, buffer, s, sub_file]
            if res is not None:
                res[3] = res[3].replace(str(_tmp), _file)
                _results.append(res)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
