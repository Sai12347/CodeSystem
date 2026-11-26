def visible():
    return [{'in': {'numCourses': 2, 'prerequisites': [[1, 0]]}}, {'in': {'numCourses': 2, 'prerequisites': [[1, 0], [0, 1]]}}, {'in': {'numCourses': 1, 'prerequisites': []}}]

def hidden():
    return [{'in': {'numCourses': 3, 'prerequisites': []}}, {'in': {'numCourses': 4, 'prerequisites': [[1, 0], [2, 1], [3, 2]]}}, {'in': {'numCourses': 3, 'prerequisites': [[0, 1], [0, 2], [1, 2]]}}, {'in': {'numCourses': 4, 'prerequisites': [[1, 0], [2, 1], [0, 2]]}}, {'in': {'numCourses': 5, 'prerequisites': [[1, 0], [2, 0], [3, 1], [3, 2]]}}, {'in': {'numCourses': 3, 'prerequisites': [[1, 0], [2, 1]]}}, {'in': {'numCourses': 4, 'prerequisites': [[1, 0], [1, 2], [3, 2]]}}, {'in': {'numCourses': 5, 'prerequisites': [[1, 0], [2, 1], [3, 2], [4, 3]]}}]
