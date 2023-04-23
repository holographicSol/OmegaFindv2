""" Written by Benjamin Jack Cullen """


def dict_maker(_recognized_files: list, _buffer_max: int, _type_suffix: list,
               _learn: bool, _de_scan: bool, _type_scan: bool, _p_scan: bool,
               _extract: bool, _target: str, _reveal_scan: bool, _program_root: str,
               _contents_scan: bool, _query: str, _verbose: bool, _human_size: bool, _digits=True) -> dict:

    multiproc_dict = {'files_recognized': _recognized_files,
                      'buffer_max': _buffer_max,
                      'target': _target,
                      'program_root': _program_root,
                      'verbose': _verbose,
                      'digits': _digits,
                      'human_size': _human_size}

    if _extract is True:
        multiproc_dict.update({'extract': True})
    if _extract is False:
        multiproc_dict.update({'extract': False})

    if _type_scan is True:
        multiproc_dict.update({'suffix': _type_suffix})

    elif _contents_scan is True:
        multiproc_dict.update({'query': _query})

    return multiproc_dict
