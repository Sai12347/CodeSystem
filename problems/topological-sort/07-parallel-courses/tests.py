def visible():
    return [{'in': {'n': 3, 'relations': [[1, 3], [2, 3]]}}, {'in': {'n': 3, 'relations': [[1, 2], [2, 3], [3, 1]]}}, {'in': {'n': 1, 'relations': []}}]

def hidden():
    return [{'in': {'n': 4, 'relations': []}}, {'in': {'n': 4, 'relations': [[1, 2], [2, 3], [3, 4]]}}, {'in': {'n': 4, 'relations': [[1, 3], [2, 3], [3, 4]]}}, {'in': {'n': 5, 'relations': [[1, 2], [1, 3], [3, 4], [2, 5]]}}, {'in': {'n': 3, 'relations': [[1, 2], [1, 3]]}}, {'in': {'n': 4, 'relations': [[1, 2], [1, 3], [2, 4], [3, 4]]}}, {'in': {'n': 3, 'relations': [[1, 2], [2, 3]]}}, {'in': {'n': 5, 'relations': [[1, 3], [2, 3], [3, 4], [3, 5]]}}]
