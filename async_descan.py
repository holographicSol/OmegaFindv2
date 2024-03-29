""" Written by Benjamin Jack Cullen """

import os
import asyncio
import handler_strings
import handler_file
import async_check
import scanfs
import handler_extraction_method


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    _extract = kwargs.get('extract')
    _digits = kwargs.get('digits')
    _human_size = kwargs.get('human_size')

    if _extract is False:
        return [await de_scan(_file=item, _recognized_files=_recognized_files, _buffer_max=_buffer_max,
                              _extract=_extract, _target=_target, _program_root=_program_root, _digits=_digits,
                              _human_size=_human_size) for item in chunk]
    elif _extract is True:
        return [await de_scan_extract(_file=item, _recognized_files=_recognized_files, _buffer_max=_buffer_max,
                                      _extract=_extract, _target=_target, _program_root=_program_root, _digits=_digits,
                                      _human_size=_human_size) for item in chunk]


async def de_scan(_file: str, _recognized_files: list, _buffer_max: int, _extract: bool, _target: str,
                  _program_root: str, _digits=True, _human_size=False) -> list:
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, _file=_file)
        _result = await async_check.scan_check(_file=_file, _suffix=suffix, _buffer=buffer,
                                               _recognized_files=_recognized_files, _digits=_digits,
                                               _human_size=_human_size)
    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    if _result:
        return _result


async def de_scan_extract(_file: str, _recognized_files: list, _buffer_max: int, _extract: bool, _target: str,
                          _program_root: str, _digits=True, _human_size=False) -> list:
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        _result = await extract_de_scan(_buffer=buffer, _file=_file, _buffer_max=_buffer_max,
                                        _recognized_files=_recognized_files, _target=_target,
                                        _program_root=_program_root, _digits=_digits, _human_size=_human_size)
    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    if _result:
        return _result


async def extract_de_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list, _target: str,
                          _program_root: str, _digits=True, _human_size=False) -> list:
    suffix = await asyncio.to_thread(handler_file.get_suffix, _file=_file)
    _results = await async_check.scan_check(_file=_file, _suffix=suffix, _buffer=_buffer,
                                            _recognized_files=_recognized_files, _digits=_digits,
                                            _human_size=_human_size)
    if _results is not None:
        _results = [_results]
    else:
        _results = []
    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        if os.path.exists(_tmp):
            sub_files = await asyncio.to_thread(scanfs.scan, _path=_tmp)
            sub_files[:] = [item for sublist in sub_files for item in sublist]
            for sub_file in sub_files:
                buffer = await handler_file.async_read_bytes(_file=sub_file, _buffer_max=_buffer_max)
                suffix = await asyncio.to_thread(handler_file.get_suffix, _file=sub_file)
                res = await async_check.scan_check(_file=sub_file, _suffix=suffix, _buffer=buffer,
                                                   _recognized_files=_recognized_files, _digits=_digits,
                                                   _human_size=_human_size)
                if res is not None:
                    res[3] = res[3].replace(str(_tmp), _file+'\\')
                    _results.append(res)
    else:
        if 'Password required' in extraction:
            _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    if _results:
        return _results
