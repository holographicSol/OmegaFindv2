import os
import handler_chunk
import asyncio
import handler_strings
import handler_file
import async_check
import scanfs

program_root = handler_file.get_executable_path()


async def entry_point_de_scan(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _extract = False
    if 'extract' in kwargs.keys():
        _extract = kwargs.get('extract')
    return [await de_scan(item, _recognized_files, _buffer_max, _extract, _target) for item in chunk]


async def de_scan(file: str, _recognized_files: list, _buffer_max: int, _extract: bool, _target: str) -> list:
    try:
        buffer = await handler_file.async_read_bytes(file, _buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, file)
        _result = await async_check.scan_check(file, suffix, buffer, _recognized_files)
        if await async_check.check_extract(_extract=_extract, _buffer=buffer) is True:
            _result = await extract_de_scan(_buffer=buffer, _file=file, _buffer_max=_buffer_max,
                                            _recognized_files=_recognized_files, _target=_target)
    except Exception as e:
        _result = [['[ERROR]', str(file), str(e)]]
    return _result


async def extract_de_scan(_buffer: bytes, _file: str, _buffer_max: int, _recognized_files: list, _target: str) -> list:
    _results = [[_file, _buffer]]
    _tmp = program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_file.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        if os.path.exists(_tmp):
            sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
            sub_files = await asyncio.to_thread(handler_chunk.un_chunk_data, sub_files, depth=1)
            for sub_file in sub_files:
                buffer = await handler_file.async_read_bytes(sub_file, _buffer_max)
                suffix = await asyncio.to_thread(handler_file.get_suffix, sub_file)
                res = await async_check.scan_check(sub_file, suffix, buffer, _recognized_files)
                if res is not None:
                    res[0] = res[0].replace(_tmp, _target)
                    _results.append(res)
    else:
        _results = extraction
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
