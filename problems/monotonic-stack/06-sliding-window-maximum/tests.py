import random


def visible():
    return [
        {"in": {"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3}},
        {"in": {"nums": [1], "k": 1}},
        {"in": {"nums": [9, 11], "k": 2}},
    ]


def hidden():
    rng = random.Random(239)
    stress_rand = [rng.randint(-10000, 10000) for _ in range(2000)]
    stress_desc = [1500 - i for i in range(1500)]
    return [
        {"in": {"nums": [4, -2, 7, 0, -5], "k": 1}},
        {"in": {"nums": [4, -2, 7, 0, -5], "k": 5}},
        {"in": {"nums": [5] * 10, "k": 4}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7, 8], "k": 3}},
        {"in": {"nums": [8, 7, 6, 5, 4, 3, 2, 1], "k": 3}},
        {"in": {"nums": [-7, -8, -7, -5, -7, -1, -6, 0], "k": 4}},
        {"in": {"nums": [1, 3, 1, 2, 0, 5], "k": 3}},
        {"in": {"nums": [-10000, 10000, -10000, 10000, -10000], "k": 2}},
        {"in": {"nums": [5, 5, 5, 1, 2, 3], "k": 3}},
        {"in": {"nums": stress_desc, "k": 400}},
        {"in": {"nums": stress_rand, "k": 150}},
    ]
