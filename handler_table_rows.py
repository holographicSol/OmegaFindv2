import handler_print


def display_rows_interactively(max_limit: int, _results: list, table: str):

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
                        input('\n--- more ---\n')
                        i_limiter = 0

        else:
            print(table)

    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass
