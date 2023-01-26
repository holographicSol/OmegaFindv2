
def result_handler(_results: list):
    if len(_results) <= 12:
        print('[Unrecognized files]:')
        for result in _results:
            print(' ', result)
    else:
        print('[Unrecognized files]:')
        i_result = 0
        for result in _results:
            if i_result <= 12:
                print(' ', result)
                i_result += 1
            else:
                break
