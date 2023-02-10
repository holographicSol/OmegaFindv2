""" Written by Benjamin Jack Cullen """
import handler_chunk
import handler_print


def dict_maker(_recognized_files: list, _buffer_max: int, _type_suffix: list,
               _learn: bool, _de_scan: bool, _type_scan: bool, _p_scan: bool,
               _extract: bool, _target: str, _reveal_scan: bool, _program_root: str) -> dict:

    multiproc_dict = {'files_recognized': _recognized_files,
                      'buffer_max': _buffer_max,
                      'target': _target,
                      'program_root': _program_root}
    if _extract is True:
        multiproc_dict.update({'extract': True})
    if _extract is False:
        multiproc_dict.update({'extract': False})

    if _type_scan is True:
        chunk_suffix = list(handler_chunk.chunk_data(data=_type_suffix, chunk_size=10))
        handler_print.display_suffixes(_msg='-- suffixes:', _list=chunk_suffix)
        multiproc_dict.update({'suffix': _type_suffix})

    return multiproc_dict
