""" Written by Benjamin Jack Cullen """

import handler_print


def more_or_next(results: list, extra_input: bool, function=None, message=''):
    if extra_input is True:
        print(message)
        function(results)
    else:
        input(message)


def display_rows_interactively(max_limit: int, results: list, table: str, extra_input: bool, message: str, function):
    """

    @param max_limit: Specify how many rows to display each iteration
    @param results: A list of Results.
    @param table: Tabular results ^.
    @param extra_input: False: Display only message. True: Display message then a run function another input function.
    @param function: Specify a module function that should request further input and do something.
    @param message: Message displayed each time rows printed reach max_limit. Example: --- more ---
    @return: None
    """
    try:
        if len(results) > max_limit:
            i_limiter = 0
            row = ''
            for char in table:

                if char == '\n':
                    if i_limiter <= max_limit:
                        # print row from table: up to max limit
                        print(row)
                        i_limiter += 1
                    else:
                        print(row)
                        # limit reached: present input
                        more_or_next(results=results, extra_input=extra_input, function=function, message=message)
                        i_limiter = 0
                    row = ''

                elif char != '\n':
                    row = row + char

        else:
            print(table)

    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass
