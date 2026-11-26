import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 1]}},
        {"in": {"nums": [2, 7, 9, 3, 1]}},
        {"in": {"nums": [2, 1, 1, 2]}},
    ]


def hidden():
    rng1 = random.Random(198)
    rng2 = random.Random(1980)
    return [
        {"in": {"nums": [5]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [3, 7]}},
        {"in": {"nums": [10, 4]}},
        {"in": {"nums": [0, 0, 0, 0, 0]}},
        {"in": {"nums": [5, 5, 5, 5, 5]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"nums": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": [100, 1, 1, 100, 1, 1, 100]}},
        {"in": {"nums": [rng1.randint(0, 500) for _ in range(18)]}},
        {"in": {"nums": [rng2.randint(0, 10000) for _ in range(3000)]}},
    ]
