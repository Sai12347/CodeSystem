import random


def visible():
    return [
        {"in": {"nums": [7, 2, 5, 10, 8], "k": 2}},
        {"in": {"nums": [1, 2, 3, 4, 5], "k": 2}},
        {"in": {"nums": [1, 4, 4], "k": 3}},
    ]


def hidden():
    rng1 = random.Random(410)
    stress1 = [rng1.randint(0, 100000) for _ in range(500)]

    rng2 = random.Random(41002)
    stress2 = [rng2.randint(0, 1000000) for _ in range(1000)]

    return [
        {"in": {"nums": [0], "k": 1}},
        {"in": {"nums": [1000000], "k": 1}},
        {"in": {"nums": [0, 0, 0, 0, 0], "k": 3}},
        {"in": {"nums": [0, 100, 0, 0, 100, 0], "k": 2}},
        {"in": {"nums": [1000000, 1000000, 1000000], "k": 1}},
        {"in": {"nums": [3, 1, 99, 2, 5], "k": 5}},
        {"in": {"nums": [5, 5, 5, 5, 5, 5, 5], "k": 3}},
        {"in": {"nums": [1000, 1, 1, 1, 1, 1, 1, 1, 1], "k": 2}},
        {"in": {"nums": stress1, "k": 20}},
        {"in": {"nums": stress2, "k": 50}},
    ]
