""" Written by Benjamin Jack Cullen """
import chunk_handler


def dict_maker(_recognized_files: list, _buffer_max: int, _type_suffix: list,
               _learn: bool, _de_scan: bool, _type_scan: bool) -> dict:
    multiproc_dict = {}

    if _learn is True or _de_scan is True:
        multiproc_dict = {'files_recognized': _recognized_files,
                          'buffer_max': _buffer_max}

    elif _type_scan is True:
        chunk_suffix = list(chunk_handler.chunk_data(data=_type_suffix, chunk_size=10))
        i = 0
        print('[Suffixes]')
        for _ in chunk_suffix:
            print('          ' + str(_))
            i += 1
        multiproc_dict = {'files_recognized': _recognized_files,
                          'buffer_max': _buffer_max,
                          'suffix': _type_suffix}
    return multiproc_dict
