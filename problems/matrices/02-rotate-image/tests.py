import random


def visible():
    return [
        {"in": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}},
        {"in": {"matrix": [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]}},
    ]


def hidden():
    rng = random.Random(4802)
    m5 = [[r * 5 + c + 1 for c in range(5)] for r in range(5)]
    m6 = [[r * 6 + c - 18 for c in range(6)] for r in range(6)]
    ident = [[1 if r == c else 0 for c in range(5)] for r in range(5)]
    stress30 = [[rng.randint(-10000, 10000) for _ in range(30)] for _ in range(30)]
    stress50 = [[rng.randint(-10000, 10000) for _ in range(50)] for _ in range(50)]
    return [
        {"in": {"matrix": [[1]]}},
        {"in": {"matrix": [[1, 2], [3, 4]]}},
        {"in": {"matrix": m5}},
        {"in": {"matrix": m6}},
        {"in": {"matrix": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]}},
        {"in": {"matrix": [[1, 2, 1], [2, 3, 2], [1, 2, 1]]}},
        {"in": {"matrix": [[-10000, 0, 10000], [-1, 50, -9999], [9999, -50, 1]]}},
        {"in": {"matrix": ident}},
        {"in": {"matrix": stress30}},
        {"in": {"matrix": stress50}},
    ]
