import handler_print
import handler_strings


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
                        if open_dir is True:
                            print('\n--- more ---\n')
                            handler_strings.input_open_dir(_list=_results)
                        else:
                            input('\n--- more ---\n')
                        i_limiter = 0
                    p = ''

                elif char != '\n':
                    p = p + char

                else:
                    if i_limiter <= max_limit:
                        print(p)
                        i_limiter += 1
                    else:
                        if open_dir is True:
                            print('\n--- more ---\n')
                            handler_strings.input_open_dir(_list=_results)
                        else:
                            input('\n--- more ---\n')
                        i_limiter = 0

        else:
            print(table)

    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass
