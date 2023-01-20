import asyncio

recognized_files = []
filtered_results = []


async def learn(_results: list):
    global recognized_files
    global filtered_results
    try:
        for _result in _results:
            check_ = [_result[1], _result[2]]
            if check_ not in recognized_files:
                if check_ not in filtered_results:
                    filtered_results.append(check_)
    except:
        pass


async def async_learn(_results: list, _recognized_files: list) -> list:
    global recognized_files
    global filtered_results
    recognized_files = _recognized_files
    filtered_results = []
    for result in _results:
        await asyncio.gather(*map(learn, [[result]]))
    return filtered_results
