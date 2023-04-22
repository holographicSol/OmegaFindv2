""" Written by Benjamin Jack Cullen """

import handler_chunk
import asyncio
import handler_strings
import handler_file
import scanfs
import handler_extraction_method


async def entry_point_mtime_scan(chunk: list, **kwargs) -> list:
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    _extract = kwargs.get('extract')

    if _extract is False:
        return [await mtime_scan(item, _extract, _target, _program_root) for item in chunk]
    elif _extract is True:
        return [await mtime_scan_extract(item, _extract, _target, _program_root) for item in chunk]


async def mtime_scan(file: str, _extract: bool, _target: str, _program_root: str) -> list:
    _result = []
    try:
        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file)
        return [m, s, file]

    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def mtime_scan_extract(file: str, _extract: bool, _target: str, _program_root: str) -> list:
    _result = []
    try:
        _result = await extract_mtime_scan(_file=file, _target=_target, _program_root=_program_root)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_mtime_scan(_file: str, _target: str, _program_root: str) -> list:
    _results = []
    m = await asyncio.to_thread(handler_file.get_m_time, _file)
    s = await asyncio.to_thread(handler_file.get_size, _file)
    _results = [[m, s, _file]]
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
        sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
        for sub_file in sub_files:
            m = await asyncio.to_thread(handler_file.get_m_time, sub_file)
            s = await asyncio.to_thread(handler_file.get_size, sub_file)
            res = [m, s, sub_file]
            if res is not None:
                res[2] = res[2].replace(str(_tmp), _target)
                _results.append(res)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
