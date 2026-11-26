def visible():
    return [{'in': {'nums': [1, 2, 3], 'sequences': [[1, 2], [1, 3]]}}, {'in': {'nums': [1, 2, 3], 'sequences': [[1, 2], [2, 3]]}}, {'in': {'nums': [1], 'sequences': [[1]]}}]

def hidden():
    return [{'in': {'nums': [1, 2], 'sequences': [[1], [2]]}}, {'in': {'nums': [1, 2], 'sequences': [[1, 2]]}}, {'in': {'nums': [2, 1], 'sequences': [[1, 2]]}}, {'in': {'nums': [1, 2, 3], 'sequences': [[1, 2, 3]]}}, {'in': {'nums': [1, 2, 3], 'sequences': [[1, 2], [2, 3], [1, 3]]}}, {'in': {'nums': [1, 2, 3], 'sequences': [[1, 2], [2, 3], [3, 1]]}}, {'in': {'nums': [1, 2, 3], 'sequences': [[1, 2], [2, 3], [1, 3], [3]]}}, {'in': {'nums': [3, 1, 2], 'sequences': [[3, 1], [1, 2]]}}]
