""" Written by Benjamin Jack Cullen

Compliment tabulate module.
Overcome potential Terminal/Console buffer limitations causing a table to not be entirely displayed.
Display N rows of table at a time, with some customization.

Simple Example:
tabulate_helper.display_rows_interactively(max_limit=75,
                                           results=_results,
                                           table=table_1,
                                           extra_input=False,
                                           message='\n--- more ---\n',
                                           function=None)
Note: Simply display rows until max_limit reached and display message.

Advanced Example:
tabulate_helper.display_rows_interactively(max_limit=75,
                                           results=a_list,
                                           table=a_table,
                                           extra_input=True,
                                           message='\n--- more ---\n',
                                           function=a_module.a_function_that_takes_input)

Note: a_function_that_takes_input may simply take digits that point at an index in results and do something.

"""

import handler_print


def more_or_next(results: list, extra_input: bool, function=None, message=''):
    # removing soon or updating so extra input is False
    extra_input = False
    if extra_input is True:
        print(message)
        function(results)
    else:
        input('-- more --')
        # input(message)


def display_rows_interactively(max_limit: int, results: list, table: str, extra_input: bool, message: str, function):
    """

    @param max_limit: Specify how many rows to display each iteration
    @param results: A list of Results.
    @param table: Tabular results ^.
    @param extra_input: False: Display only message. True: Display message then a run another (input) function.
    @param function: Specify a module function that should request further input and do something. Note:
                     argument=results^ are passed through to argument=function^ specified.
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
            if extra_input is True:
                more_or_next(results=results, extra_input=extra_input, function=function, message=message)

    except KeyboardInterrupt:
        handler_print.display_spacer()
        pass
