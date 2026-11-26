import random


def visible():
    return [
        {"in": {"nums": [1, 1, 1], "k": 2}},
        {"in": {"nums": [1, 2, 3], "k": 3}},
        {"in": {"nums": [1, -1, 0], "k": 0}},
    ]


def hidden():
    rng = random.Random(560)
    big_random = [rng.randint(-50, 50) for _ in range(1500)]
    big_zeros = [0] * 1000
    alternating = [1 if i % 2 == 0 else -1 for i in range(1200)]
    return [
        {"in": {"nums": [5], "k": 5}},
        {"in": {"nums": [5], "k": 0}},
        {"in": {"nums": [0], "k": 0}},
        {"in": {"nums": [0, 0, 0, 0, 0], "k": 0}},
        {"in": {"nums": [-1, -1, 1], "k": 0}},
        {"in": {"nums": [-1, -1, -1], "k": -2}},
        {"in": {"nums": [3, 4, 7, 2, -3, 1, 4, 2], "k": 7}},
        {"in": {"nums": [1000, 1000, 1000], "k": 10000000}},
        {"in": {"nums": [-1000, -1000, -1000], "k": -3000}},
        {"in": {"nums": alternating, "k": 0}},
        {"in": {"nums": big_zeros, "k": 0}},
        {"in": {"nums": big_random, "k": 25}},
    ]
