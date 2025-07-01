from googlesearch import search

def googling(query, length = 5):
    results = []
    for result in search(query, num_results = length):
        results.append(result)
    return results