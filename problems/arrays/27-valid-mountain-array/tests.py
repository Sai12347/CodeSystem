def visible():
    return [{'in': {'arr': [0, 3, 2, 1]}, 'out': True}, {'in': {'arr': [3, 5, 5]}, 'out': False}, {'in': {'arr': [2, 1]}, 'out': False}]

def hidden():
    return [{'in': {'arr': [0, 1, 2, 3]}, 'out': False}, {'in': {'arr': [3, 2, 1, 0]}, 'out': False}, {'in': {'arr': [0, 2, 1]}, 'out': True}, {'in': {'arr': [1, 2, 2, 1]}, 'out': False}, {'in': {'arr': [0, 1, 2, 1, 0]}, 'out': True}, {'in': {'arr': [1, 3, 2, 1, 0]}, 'out': True}, {'in': {'arr': [1, 2, 1, 2]}, 'out': False}, {'in': {'arr': [0, 1, 0]}, 'out': True}]
