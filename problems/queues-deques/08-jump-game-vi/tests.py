import random


def visible():
    return [
        {"in": {"nums": [1, -1, -2, 4, -7, 3], "k": 2}},
        {"in": {"nums": [10, -5, -2, 4, 0, 3], "k": 3}},
        {"in": {"nums": [1, -5, -20, 4, -1, 3, -6, -3], "k": 2}},
    ]


def hidden():
    rng1 = random.Random(1696)
    big1 = [rng1.randint(-10000, 10000) for _ in range(2500)]

    rng2 = random.Random(16960)
    big2 = [rng2.randint(-10000, -1) if rng2.random() < 0.85 else rng2.randint(0, 5000) for _ in range(2500)]

    return [
        {"in": {"nums": [5], "k": 1}},
        {"in": {"nums": [-10000], "k": 5}},
        {"in": {"nums": [3, -5, 2, -8, 4], "k": 1}},
        {"in": {"nums": [-5, -10, -2, -100, -3], "k": 10}},
        {"in": {"nums": [-1, -2, -3, -4, -5, -6, -7, -8], "k": 3}},
        {"in": {"nums": [0] * 15, "k": 4}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}},
        {"in": {"nums": [10000, -10000, -10000, 10000, -10000, 10000], "k": 2}},
        {"in": {"nums": [10, -100, 20, -100, 30, -100, 40], "k": 2}},
        {"in": {"nums": big1, "k": 50}},
        {"in": {"nums": big2, "k": 300}},
    ]
