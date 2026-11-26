import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3]}},
        {"in": {"nums": [0, 1]}},
        {"in": {"nums": [1]}},
    ]


def hidden():
    rng = random.Random(46)
    rand6 = rng.sample(range(-10, 11), 6)
    return [
        {"in": {"nums": [-10]}},
        {"in": {"nums": [-5, -1]}},
        {"in": {"nums": [3, 2, 1]}},
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [-10, 0, 5, 10]}},
        {"in": {"nums": [5, -2, 3, -4, 1]}},
        {"in": {"nums": [10, 5, 0, -5, -10]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6]}},
        {"in": {"nums": [6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": rand6}},
    ]
