import random


def visible():
    return [
        {"in": {"nums": [2, 3, 2]}},
        {"in": {"nums": [1, 2, 3, 1]}},
        {"in": {"nums": [1, 2, 3]}},
    ]


def hidden():
    rng1 = random.Random(213)
    rng2 = random.Random(2130)
    return [
        {"in": {"nums": [7]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [4, 9]}},
        {"in": {"nums": [6, 6]}},
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [100, 1, 1, 100]}},
        {"in": {"nums": [200, 3, 140, 20, 10]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7]}},
        {"in": {"nums": [7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": [rng1.randint(0, 500) for _ in range(18)]}},
        {"in": {"nums": [rng2.randint(0, 10000) for _ in range(3000)]}},
    ]
