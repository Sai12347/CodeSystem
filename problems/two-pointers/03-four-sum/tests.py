import random


def visible():
    return [
        {"in": {"nums": [1, 0, -1, 0, -2, 2], "target": 0}},
        {"in": {"nums": [2, 2, 2, 2, 2], "target": 8}},
        {"in": {"nums": [1, 2, 3], "target": 6}},
    ]


def hidden():
    rng1 = random.Random(301)
    arr1 = [rng1.randint(-500, 500) for _ in range(70)]

    rng2 = random.Random(302)
    arr2 = [rng2.randint(-50000, 50000) for _ in range(140)]

    return [
        {"in": {"nums": [0], "target": 0}},
        {"in": {"nums": [-5, 2, 1, 2], "target": 0}},
        {"in": {"nums": [1, 2, 3, 4], "target": 11}},
        {"in": {"nums": [0, 0, 0, 0, 0, 0], "target": 0}},
        {"in": {"nums": [1000000000, 1000000000, 1000000000, 1000000000], "target": -294967296}},
        {"in": {"nums": [-1000000000, -1000000000, -1000000000, -1000000000], "target": 294967296}},
        {"in": {"nums": [-1000000000, -1000000000, 1000000000, 1000000000, 0, 0], "target": 0}},
        {"in": {"nums": [-3, -2, -1, 0, 0, 1, 2, 3, -3, 3], "target": 0}},
        {"in": {"nums": [10, 8, 6, 4, 2, 0, -2, -4, -6, -8, -10], "target": -12}},
        {"in": {"nums": arr1, "target": 42}},
        {"in": {"nums": arr2, "target": 0}},
    ]
