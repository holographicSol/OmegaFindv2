""" Written by Benjamin Jack Cullen """

import asyncio
import handler_file
import async_check
import handler_strings
import handler_extraction_method
import scanfs

x_learn = []


async def entry_point_learn(chunk: list, **kwargs) -> list:
    _recognized_files = kwargs.get('files_recognized')
    _buffer_max = int(kwargs.get('buffer_max'))
    _target = str(kwargs.get('target'))
    _program_root = str(kwargs.get('program_root'))
    _extract = kwargs.get('extract')
    if _extract is False:
        return [await scan_learn(_file=item,
                                 _recognized_files=_recognized_files,
                                 _target=_target, _buffer_max=_buffer_max,
                                 _program_root=_program_root, _extract=_extract) for item in chunk]
    elif _extract is True:
        return [await extract_learn(_file=item,
                                    _recognized_files=_recognized_files,
                                    _target=_target, _buffer_max=_buffer_max,
                                    _program_root=_program_root, _extract=_extract) for item in chunk]


async def scan_learn_check(_suffix: str, _buffer: bytes, _recognized_files: list) -> list:
    global x_learn
    assoc = [_suffix, _buffer]
    if await async_check.check_not_in_list(_list_1=assoc, _list_2=x_learn) is False:
        x_learn.append(assoc)
        if await async_check.check_not_in_list(_list_1=assoc, _list_2=_recognized_files) is False:
            return assoc


async def scan_learn(_file: str, _recognized_files: list, _target: str, _buffer_max: int,
                     _program_root: str, _extract: bool) -> list:
    try:
        buffer = await handler_file.async_read_bytes(_file=_file, _buffer_max=_buffer_max)
        suffix = await asyncio.to_thread(handler_file.get_suffix, _file=_file)
        _result = await scan_learn_check(_suffix=suffix, _buffer=buffer, _recognized_files=_recognized_files)
    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    return _result


async def extract_learn(_file: str, _recognized_files: list, _target: str, _buffer_max: int,
                        _program_root: str, _extract: bool) -> list:

    _results = [await scan_learn(_file=_file,
                                 _recognized_files=_recognized_files,
                                 _target=_target, _buffer_max=_buffer_max,
                                 _program_root=_program_root, _extract=_extract)]

    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _path=_tmp)
        sub_files[:] = [item for sublist in sub_files for item in sublist]
        for sub_file in sub_files:
            res = await scan_learn(_file=sub_file,
                                   _recognized_files=_recognized_files,
                                   _target=_target, _buffer_max=_buffer_max,
                                   _program_root=_program_root, _extract=_extract)
            if res is not None:
                _results.append(res)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)

    return _results
