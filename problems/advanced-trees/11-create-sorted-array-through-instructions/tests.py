def visible():
    return [{'in': {'instructions': [1, 5, 6, 2]}}, {'in': {'instructions': [1, 2, 3, 6, 5, 4]}}, {'in': {'instructions': [1, 3, 3, 3, 2, 4, 2, 1, 2]}}]

def hidden():
    return [{'in': {'instructions': [1]}}, {'in': {'instructions': [2, 1]}}, {'in': {'instructions': [5, 5, 5]}}, {'in': {'instructions': [1, 2, 1, 2]}}, {'in': {'instructions': [100000, 1, 100000]}}, {'in': {'instructions': [2, 1, 3, 1, 2]}}, {'in': {'instructions': [10, 9, 8, 7, 6]}}, {'in': {'instructions': [1, 100, 2, 99, 3]}}]
