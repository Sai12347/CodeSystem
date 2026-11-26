def visible():
    return [{'in': {'heights': [1, 1, 4, 2, 1, 3]}, 'out': 3}, {'in': {'heights': [5, 1, 2, 3, 4]}, 'out': 5}, {'in': {'heights': [1, 2, 3, 4, 5]}, 'out': 0}]

def hidden():
    return [{'in': {'heights': [1]}, 'out': 0}, {'in': {'heights': [2, 1]}, 'out': 2}, {'in': {'heights': [3, 3, 3]}, 'out': 0}, {'in': {'heights': [4, 1, 2, 3, 3]}, 'out': 4}, {'in': {'heights': [10, 20, 30, 40]}, 'out': 0}, {'in': {'heights': [100, 1, 50, 2]}, 'out': 3}, {'in': {'heights': [4, 3, 2, 1]}, 'out': 4}, {'in': {'heights': [2, 1, 2, 1]}, 'out': 2}]
