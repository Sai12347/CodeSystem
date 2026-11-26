def visible():
    return [{'in': {'nums': [1, 2, 2, 3]}, 'out': True}, {'in': {'nums': [1, 3, 2]}, 'out': False}, {'in': {'nums': [6, 5, 4, 4]}, 'out': True}]

def hidden():
    return [{'in': {'nums': [1]}, 'out': True}, {'in': {'nums': [2, 2, 2]}, 'out': True}, {'in': {'nums': [-3, -2, -1]}, 'out': True}, {'in': {'nums': [9, 7, 5, 3]}, 'out': True}, {'in': {'nums': [1, 2, 1, 0]}, 'out': False}, {'in': {'nums': [0, 0, 1, 1, 2]}, 'out': True}, {'in': {'nums': [3, 2, 1, 2]}, 'out': False}, {'in': {'nums': [5, 4, 4, 1]}, 'out': True}]
