import random


def visible():
    return [
        {"in": {"nums": [1, 2, 1, 2, 3], "k": 2}},
        {"in": {"nums": [1, 2, 1, 3, 4], "k": 3}},
        {"in": {"nums": [1, 1, 1], "k": 1}},
    ]


def hidden():
    rng1 = random.Random(992)
    stress1 = [rng1.randint(1, 25) for _ in range(2500)]

    stress2 = [1] * 2000

    return [
        {"in": {"nums": [1], "k": 1}},
        {"in": {"nums": [1, 1, 1, 1], "k": 2}},
        {"in": {"nums": [1, 2, 3, 4, 5], "k": 5}},
        {"in": {"nums": [1, 2, 3, 4, 1], "k": 5}},
        {"in": {"nums": [1, 1, 2, 2, 2, 1, 3], "k": 1}},
        {"in": {"nums": [1, 2, 1, 2, 1, 2], "k": 2}},
        {"in": {"nums": [2, 1, 1, 1, 2], "k": 1}},
        {"in": {"nums": [6, 5, 6, 4, 5, 6], "k": 3}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "k": 4}},
        {"in": {"nums": stress1, "k": 10}},
        {"in": {"nums": stress2, "k": 1}},
    ]
