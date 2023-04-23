import handler_file
import power_converter


def convert_results(_results, _human_size=False, _mtime_scan=False):
    n_result = 0
    for sublist in _results:
        sublist[0] = handler_file.convert_timestamp_to_datetime(float(sublist[0]))
        if _human_size is True:
            if _mtime_scan is False:
                sublist[2] = str(power_converter.convert_bytes(*[int(sublist[2])], abbr=True)[0])
            else:
                sublist[1] = str(power_converter.convert_bytes(*[int(sublist[1])], abbr=True)[0])
        n_result += 1
    return _results


def convert_string_match_results(_results, _human_size=False):
    n_result = 0
    for sublist in _results:
        # print(sublist)
        sublist[1] = handler_file.convert_timestamp_to_datetime(float(sublist[1]))
        if _human_size is True:
            sublist[2] = str(power_converter.convert_bytes(*[int(sublist[2])], abbr=True)[0])
        n_result += 1
    return _results
