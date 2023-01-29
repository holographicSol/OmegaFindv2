""" Written by Benjamin Jack Cullen """
import handler_chunk


def dict_maker(_recognized_files: list, _buffer_max: int, _type_suffix: list,
               _learn: bool, _de_scan: bool, _type_scan: bool,
               _extract: bool) -> dict:
    multiproc_dict = {'files_recognized': _recognized_files,
                      'buffer_max': _buffer_max}

    if _extract is True:
        multiproc_dict.update({'extract': True})

    if _type_scan is True:
        chunk_suffix = list(handler_chunk.chunk_data(data=_type_suffix, chunk_size=10))
        i = 0
        print('-- suffixes:')
        for _ in chunk_suffix:
            print('    ' + str(_))
            i += 1
        multiproc_dict.update({'suffix': _type_suffix})
    return multiproc_dict
