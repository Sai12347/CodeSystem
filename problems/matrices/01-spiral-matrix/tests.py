import random


def visible():
    return [
        {"in": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}},
        {"in": {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]}},
        {"in": {"matrix": [[10, -5, 0, 7]]}},
    ]


def hidden():
    rng = random.Random(5401)
    stress_sq = [[rng.randint(-10000, 10000) for _ in range(40)] for _ in range(40)]
    stress_rect = [[rng.randint(-10000, 10000) for _ in range(50)] for _ in range(35)]
    return [
        {"in": {"matrix": [[42]]}},
        {"in": {"matrix": [[1], [2], [3], [4], [5]]}},
        {"in": {"matrix": [[1, 2], [3, 4]]}},
        {"in": {"matrix": [[1, 2], [3, 4], [5, 6], [7, 8]]}},
        {"in": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]}},
        {"in": {"matrix": [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]}},
        {"in": {"matrix": [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]}},
        {"in": {"matrix": [[7, 7, 7], [7, 7, 7], [7, 7, 7]]}},
        {"in": {"matrix": [[-10000, 0, 10000, -1], [5, -5, 5, -5], [10000, -10000, 0, 1]]}},
        {"in": {"matrix": stress_sq}},
        {"in": {"matrix": stress_rect}},
    ]
