def visible():
    return [{'in': {'changed': [1, 3, 4, 2, 6, 8]}}, {'in': {'changed': [6, 3, 0, 1]}}, {'in': {'changed': []}}]

def hidden():
    return [{'in': {'changed': [0, 0]}}, {'in': {'changed': [0, 0, 0, 0]}}, {'in': {'changed': [1, 2]}}, {'in': {'changed': [1, 2, 3]}}, {'in': {'changed': [2, 4, 8, 16]}}, {'in': {'changed': [4, 2, 8, 4]}}, {'in': {'changed': [1, 2, 2, 4]}}, {'in': {'changed': [1, 10, 3, 7, 20, 6]}}, {'in': {'changed': [5, 5, 10, 10]}}]
