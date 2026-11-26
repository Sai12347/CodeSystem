import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [-1, 2]}},
    ]


def hidden():
    rng = random.Random(78)
    rand8 = rng.sample(range(-10, 11), 8)
    return [
        {"in": {"nums": [-10]}},
        {"in": {"nums": [5, -5]}},
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [4, 3, 2, 1]}},
        {"in": {"nums": [-10, 0, 10]}},
        {"in": {"nums": [-8, -5, -2, -1]}},
        {"in": {"nums": [7, -3, 0, 4, -9]}},
        {"in": {"nums": [10, -10, 5, -5, 1, -1]}},
        {"in": {"nums": rand8}},
        {"in": {"nums": [-10, -8, -5, -2, 0, 1, 3, 6, 8, 10]}},
    ]
