""" Written by Benjamin Jack Cullen """

import asyncio
import handler_strings
import handler_file
import async_check
import scanfs
import handler_extraction_method


async def entry_point_type_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _type_suffix = kwargs.get('suffix')
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    _extract = kwargs.get('extract')
    _digits = kwargs.get('digits')
    human_size = kwargs.get('human_size')

    if _extract is False:
        return [await type_scan(item, _recognized_files, _buffer_max, _type_suffix, _target, _program_root,
                                _digits, human_size) for item in chunk]
    elif _extract is True:
        return [await type_scan_extract(item, _recognized_files, _buffer_max, _type_suffix, _target, _program_root,
                                        _digits, human_size) for item in chunk]


async def type_scan(file: str, _recognized_files: list, _buffer_max: int, _type_suffix: list,
                    _target: str, _program_root: str, _digits=True, human_size=False):
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        _result = await async_check.type_scan_check(file, buffer, _recognized_files, _digits, human_size)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def type_scan_extract(file: str, _recognized_files: list, _buffer_max: int, _type_suffix: list,
                            _target: str, _program_root: str, _digits=True, human_size=False):
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        _result = await extract_type_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max,
                                          _recognized_files=_recognized_files, _type_suffix=_type_suffix,
                                          _target=_target, _program_root=_program_root, human_size=human_size)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_type_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list,
                            _type_suffix: list, _target: str, _program_root: str, _digits=True,
                            human_size=False) -> list:
    _results = []
    if [_buffer] in _recognized_files:
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
            res = await async_check.type_scan_check(sub_file, buffer, _recognized_files, _digits, human_size=human_size)
            if res is not None:
                res[3] = res[3].replace(_tmp, _target)
                _results.append(res)
    else:
        _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
