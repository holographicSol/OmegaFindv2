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
    _human_size = kwargs.get('human_size')

    if _extract is False:
        return [await type_scan(_file=item, _recognized_files=_recognized_files, _buffer_max=_buffer_max,
                                _type_suffix=_type_suffix, _target=_target, _program_root=_program_root,
                                _digits=_digits, _human_size=_human_size) for item in chunk]
    elif _extract is True:
        return [await extract_type_scan(_file=item, _buffer_max=_buffer_max, _recognized_files=_recognized_files,
                                        _type_suffix=_type_suffix, _target=_target, _program_root=_program_root,
                                        _digits=_digits, _human_size=_human_size) for item in chunk]


async def type_scan(_file: str, _recognized_files: list, _buffer_max: int, _type_suffix: list,
                    _target: str, _program_root: str, _digits=True, _human_size=False):
    try:
        buffer = await handler_file.async_read_bytes(file=_file, _buffer_max=_buffer_max)
        _result = await async_check.type_scan_check(file=_file, buffer=buffer, _recognized_files=_recognized_files,
                                                    _digits=_digits, human_size=_human_size)
    except Exception as e:
        _result = [['[ERROR]', str(_file), str(e)]]
    return _result


async def extract_type_scan(_file: str, _buffer_max: int, _recognized_files: list,
                            _type_suffix: list, _target: str, _program_root: str, _digits=True,
                            _human_size=False) -> list:

    _results = [await type_scan(_file=_file, _recognized_files=_recognized_files, _buffer_max=_buffer_max,
                                _type_suffix=_type_suffix, _target=_target, _program_root=_program_root,
                                _digits=_digits, _human_size=_human_size)]

    _tmp = _program_root+'\\tmp\\'+str(handler_strings.randStr())
    result_bool, extraction = await asyncio.to_thread(handler_extraction_method.extract_nested_compressed,
                                                      file=_file, temp_directory=_tmp, _target=_target,
                                                      _static_tmp=_tmp)
    if result_bool is True:
        sub_files = await asyncio.to_thread(scanfs.scan, _tmp)
        sub_files[:] = [item for sublist in sub_files for item in sublist]
        for sub_file in sub_files:
            res = await type_scan(_file=sub_file, _recognized_files=_recognized_files, _buffer_max=_buffer_max,
                                  _type_suffix=_type_suffix, _target=_target, _program_root=_program_root,
                                  _digits=_digits, _human_size=_human_size)
            if res is not None:
                if len(res) == 4:
                    res[3] = res[3].replace(str(_tmp), _target)
                    _results.append(res)
    await asyncio.to_thread(handler_file.rem_dir, path=_tmp)
    return _results
