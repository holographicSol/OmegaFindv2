""" Written by Benjamin Jack Cullen """

import handler_chunk
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
        return [await reveal_scan(item, _buffer_max, _extract, _target, _program_root, human_size) for item in chunk]
    elif _extract is True:
        return [await reveal_scan_extract(item, _buffer_max, _extract, _target, _program_root,
                                          human_size) for item in chunk]


async def reveal_scan(file: str, _buffer_max: int, _extract: bool, _target: str, _program_root: str,
                      human_size=False) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)

        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file, human_size)
        return [m, buffer, s, file]

    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def reveal_scan_extract(file: str, _buffer_max: int, _extract: bool, _target: str, _program_root: str,
                              human_size=False) -> list:
    _result = []
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        _result = await extract_reveal_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max, _target=_target,
                                            _program_root=_program_root, human_size=human_size)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_reveal_scan(_buffer: bytes, _file: str, _buffer_max: int, _target: str, _program_root: str,
                              human_size=False) -> list:
    _results = []
    m = await asyncio.to_thread(handler_file.get_m_time, _file)
    s = await asyncio.to_thread(handler_file.get_size, _file, human_size)
    _results = [[m, _buffer, s, _file]]
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
        # sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
        sub_files[:] = [item for sublist in sub_files for item in sublist]
        for sub_file in sub_files:
            buffer = await handler_file.async_read_bytes(sub_file, _buffer_max)
            m = await asyncio.to_thread(handler_file.get_m_time, sub_file)
            s = await asyncio.to_thread(handler_file.get_size, sub_file, human_size)
            res = [m, buffer, s, sub_file]
            if res is not None:
                res[3] = res[3].replace(str(_tmp), _target)
                _results.append(res)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
