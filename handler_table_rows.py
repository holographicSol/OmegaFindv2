import handler_print
import handler_strings


def call_input_open_dir(_results):
    if handler_strings.input_open_dir(_list=_results) is True:
        call_input_open_dir(_results)


def more_or_next(_results, open_dir):
    if open_dir is True:
        print('\n--- more ---\n')
        call_input_open_dir(_results)
    else:
        input('\n--- more ---\n')


def display_rows_interactively(max_limit: int, _results: list, table: str, open_dir: bool):

    try:
        if len(_results) > max_limit:
            i_limiter = 0
            p = ''
            for char in table:

                if char == '\n':
                    if i_limiter <= max_limit:
                        print(p)
                        i_limiter += 1
                    else:
                        more_or_next(_results, open_dir)
                        i_limiter = 0
                    p = ''

                elif char != '\n':
                    p = p + char

                else:
                    if i_limiter <= max_limit:
                        print(p)
                        i_limiter += 1
                    else:
                        more_or_next(_results, open_dir)

                        i_limiter = 0

        else:
            print(table)

    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass
