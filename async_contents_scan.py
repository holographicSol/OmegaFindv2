""" Written by Benjamin Jack Cullen """

import os
import asyncio
import handler_file
import handler_strings
import handler_extraction_method
import scanfs
import handler_chunk

x_learn = []


async def entry_point_contents_scan(chunk: list, **kwargs) -> list:
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    _extract = kwargs.get('extract')
    _query = kwargs.get('query')
    verbose = kwargs.get('verbose')
    human_size = kwargs.get('human_size')
    if _extract is False:
        return [await contents_scan(file=item, _query=_query, _verbose=verbose, _buffer_max=_buffer_max,
                                    _program_root=_program_root, human_size=human_size) for item in chunk]
    elif _extract is True:
        return [await contents_scan_extract(_file=item, _query=_query, _verbose=verbose,
                                            _buffer_max=_buffer_max, _program_root=_program_root,
                                            _target=_target, human_size=human_size) for item in chunk]


async def contents_scan(file: str, _query: str, _verbose: bool, _buffer_max: int, _program_root: str,
                        human_size=False) -> list:
    _result = ''
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        m = await asyncio.to_thread(handler_file.get_m_time, file)
        s = await asyncio.to_thread(handler_file.get_size, file, human_size)
        _result = await handler_file.file_reader(file=file, _query=_query, _verbose=_verbose, _buffer=str(buffer),
                                                 _program_root=_program_root)
        res = [m, buffer, s, _result[0]]
        return res
    except Exception as e:
        pass
        # _result = ['[ERROR]', str(file), str(e)]


async def contents_scan_extract(_file: str, _query: str, _verbose: bool, _buffer_max: int, _program_root: str,
                                _target: str, human_size=False) -> list:
    try:
        _result = await extract_contents_scan(_file, _query, _verbose, _buffer_max, _program_root, _target, human_size)
        return _result
    except Exception as e:
        pass
        # _result = ['[ERROR]', str(_file), str(e)]


async def extract_contents_scan(_file: str, _query: str, _verbose: bool, _buffer_max: int, _program_root: str,
                                _target: str, human_size=False) -> list:
    _results = await contents_scan(file=_file, _query=_query, _verbose=_verbose, _buffer_max=_buffer_max,
                                   _program_root=_program_root, human_size=human_size)
    if _results is not None:
        if '[ERROR]' not in _results[0]:
            _results = [_results]
        else:
            _results = []
    else:
        _results = []

    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        if os.path.exists(_tmp):
            sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
            sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
            # sub_files[:] = [item for sublist in sub_files for item in sublist]
            for sub_file in sub_files:
                res = await contents_scan(file=sub_file, _query=_query, _verbose=_verbose, _buffer_max=_buffer_max,
                                          _program_root=_program_root, human_size=human_size)
                if res is not None:
                    res[-1] = res[-1].replace(_tmp, _target)
                    _results.append(res)
    else:
        if 'Password required' in extraction:
            _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
