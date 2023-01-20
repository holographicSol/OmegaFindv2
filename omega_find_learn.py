

def learn(data: list) -> list:
    filtered_results = []
    for result in data:
        try:
            check_ = [result[1], result[2]]
            if check_ not in data:
                if check_ not in filtered_results:
                    filtered_results.append([result[1], result[2]])
        except:
            pass
    return filtered_results
