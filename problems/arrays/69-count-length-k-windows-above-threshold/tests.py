def visible():
    return [{'in': {'nums': [2, 2, 2, 2, 5, 5, 5, 8], 'k': 3, 'threshold': 4}}, {'in': {'nums': [1, 1, 1, 1], 'k': 2, 'threshold': 2}}, {'in': {'nums': [1], 'k': 1, 'threshold': 1}}]

def hidden():
    return [{'in': {'nums': [1, 2, 3], 'k': 1, 'threshold': 2}}, {'in': {'nums': [-1, -2, -3], 'k': 2, 'threshold': -2}}, {'in': {'nums': [5, 5, 5, 5], 'k': 2, 'threshold': 5}}, {'in': {'nums': [1, 2, 3, 4, 5], 'k': 3, 'threshold': 3}}, {'in': {'nums': [0, 0, 0], 'k': 2, 'threshold': 0}}, {'in': {'nums': [3, 1, 2, 4, 1], 'k': 2, 'threshold': 3}}, {'in': {'nums': [10, -10, 10, -10], 'k': 2, 'threshold': 0}}, {'in': {'nums': [100000, -100000, 100000], 'k': 1, 'threshold': 50000}}]
