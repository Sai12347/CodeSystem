import random


def visible():
    return [
        {"in": {"nums": [1, 2, 2]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [4, 4, 4, 1, 4]}},
    ]


def hidden():
    rng = random.Random(90)
    rand8 = [rng.choice([-3, -1, 0, 2, 2, 5]) for _ in range(8)]
    return [
        {"in": {"nums": [-10]}},
        {"in": {"nums": [2, 2, 2, 2, 2]}},
        {"in": {"nums": [7] * 10}},
        {"in": {"nums": [3, 1, 2]}},
        {"in": {"nums": [3, 3, 2, 2, 1, 1]}},
        {"in": {"nums": [-1, 0, -1, 0, 1]}},
        {"in": {"nums": [-10, -10, 10, 10]}},
        {"in": {"nums": [5, -5, 5, -5, 5]}},
        {"in": {"nums": rand8}},
        {"in": {"nums": [-10, -10, -3, 0, 0, 2, 5, 5, 10, 10]}},
    ]
