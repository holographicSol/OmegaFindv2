""" Written by Benjamin Jack Cullen """

import textwrap


def add_padding_and_new_lines_to_columns(data: list, col_idx: int, max_column_width=None, padding_left=True) -> list:
    """ Accepts data as a list of lists [ [1,2,3], [1,2,3] ] """

    _results = data

    # max_column_width is not set so set max_column_width using col_idx
    if max_column_width is None:
        max_column_width = 0
        for r in _results:
            if len(str(r[col_idx])) > max_column_width:
                max_column_width = len(str(r[col_idx]))

    # add padding and newlines for specified col_idx
    n_result = 0
    for r in _results:
        # isolate item length
        len_r = len(str(r[col_idx]))
        if len_r < max_column_width:
            # add padding
            if padding_left is True:
                _results[n_result][col_idx] = str(' ' * int(max_column_width - len_r)) + str(r[col_idx])
            else:
                _results[n_result][col_idx] = str(r[col_idx]) + str(' ' * int(max_column_width - len_r))
        else:
            # break into chunks of max_column_width and add new lines
            tmp = textwrap.wrap(str(r[col_idx]), max_column_width, replace_whitespace=False)
            new_item = tmp[0]
            n_tmp = 0
            for x in tmp:
                if n_tmp != 0:
                    new_item = new_item + '\n' + x
                n_tmp += 1
            # put back into the sub list
            _results[n_result][col_idx] = new_item
        n_result += 1

    # return the formatted data
    return _results
