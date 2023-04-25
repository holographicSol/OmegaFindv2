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
    _bench = kwargs.get('bench')
    if _extract is False:
        return [await contents_scan(_file=item, _query=_query, _verbose=verbose, _buffer_max=_buffer_max,
                                    _program_root=_program_root, human_size=human_size,
                                    _bench=_bench) for item in chunk]
    elif _extract is True:
        return [await contents_scan_extract(_file=item, _query=_query, _verbose=verbose,
                                            _buffer_max=_buffer_max, _program_root=_program_root,
                                            _target=_target, human_size=human_size,
                                            _bench=_bench) for item in chunk]


async def contents_scan(_file: str, _query: str, _verbose: bool, _buffer_max: int, _program_root: str,
                        _bench: bool, human_size=False) -> list:
    _result = ''
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        m = await asyncio.to_thread(handler_file.get_m_time, _file=_file)
        s = await asyncio.to_thread(handler_file.get_size, _file=_file)
        _result = await handler_file.file_reader(file=_file, _query=_query, _verbose=_verbose, _buffer=str(buffer),
                                                 _program_root=_program_root, _bench=_bench)
        if _result:
            res = [m, buffer, s, _result[0]]
            print(res)
            return res
    except Exception as e:
        print(e)
        return [['[ERROR]', str(_file), str(e)]]


async def contents_scan_extract(_file: str, _query: str, _verbose: bool, _buffer_max: int, _program_root: str,
                                _target: str, _bench: bool, human_size=False) -> list:
    try:
        _result = await extract_contents_scan(_file=_file, _query=_query, _verbose=_verbose, _buffer_max=_buffer_max,
                                              _program_root=_program_root, _target=_target,
                                              _bench=_bench, human_size=human_size)
        if _result is not None:
            return _result
    except Exception as e:
        print('[ERROR]', str(_file), str(e))
        return [['[ERROR]', str(_file), str(e)]]


async def extract_contents_scan(_file: str, _query: str, _verbose: bool, _buffer_max: int, _program_root: str,
                                _target: str, _bench: bool, human_size=False) -> list:

    _results = await contents_scan(_file=_file, _query=_query, _verbose=_verbose, _buffer_max=_buffer_max,
                                   _program_root=_program_root, _bench=_bench, human_size=human_size)
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
            sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, data=sub_files, depth=1)
            for sub_file in sub_files:
                res = await contents_scan(_file=sub_file, _query=_query, _verbose=_verbose, _buffer_max=_buffer_max,
                                          _program_root=_program_root, _bench=_bench, human_size=human_size)
                if res is not None:
                    try:
                        if len(res) == 4:
                            res[-1] = res[-1].replace(_tmp, _file)
                            _results.append(res)
                    except Exception as e:
                        print(f'[ERROR] ({e}): {res}')
                        res = [['[ERROR]', str(_file), str(e)]]
                        _results.append(res)
    # else:
    #     if 'Password required' in extraction:
    #         _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
