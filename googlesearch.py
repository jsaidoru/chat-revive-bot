from googlesearch import search

def googling(query, length):
    results = []
    for result in search(query, num_results = length):
        results.append(result)
    return results