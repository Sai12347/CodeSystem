import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3]}},
        {"in": {"nums": [3, 2, 1]}},
        {"in": {"nums": [1, 1, 5]}},
    ]


def hidden():
    rng = random.Random(31)
    rand_100 = [rng.randint(0, 100) for _ in range(100)]
    return [
        {"in": {"nums": [5]}},
        {"in": {"nums": [1, 2]}},
        {"in": {"nums": [2, 1]}},
        {"in": {"nums": [4, 4, 4, 4]}},
        {"in": {"nums": [1, 5, 1]}},
        {"in": {"nums": [2, 3, 1, 3, 3]}},
        {"in": {"nums": [1, 3, 2]}},
        {"in": {"nums": [1, 2, 7, 6, 5, 4, 3]}},
        {"in": {"nums": list(range(100, 0, -1))}},
        {"in": {"nums": rand_100}},
    ]
