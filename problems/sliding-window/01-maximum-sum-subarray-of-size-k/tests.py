import random


def visible():
    return [
        {"in": {"nums": [2, 1, 5, 1, 3, 2], "k": 3}},
        {"in": {"nums": [2, 3, 4, 1, 5], "k": 2}},
        {"in": {"nums": [-5, -2, -8, -1, -4], "k": 2}},
    ]


def hidden():
    rng1 = random.Random(101)
    stress1 = [rng1.randint(-10000, 10000) for _ in range(3000)]

    rng2 = random.Random(102)
    stress2 = [rng2.randint(-10000, 10000) for _ in range(3500)]

    return [
        {"in": {"nums": [42], "k": 1}},
        {"in": {"nums": [-10000], "k": 1}},
        {"in": {"nums": [-3, 10, -2, 7, -1], "k": 5}},
        {"in": {"nums": [0, 0, 0, 0, 0], "k": 3}},
        {"in": {"nums": [-7, -7, -7, -7], "k": 2}},
        {"in": {"nums": [100, 90, 80, -50, -50, -50], "k": 3}},
        {"in": {"nums": [-50, -50, -50, 80, 90, 100], "k": 3}},
        {"in": {"nums": [10000, 10000, -10000, 10000, 10000, 10000], "k": 3}},
        {"in": {"nums": [50, 40, 30, 20, 10, 0, -10, -20], "k": 4}},
        {"in": {"nums": stress1, "k": 500}},
        {"in": {"nums": stress2, "k": 1}},
    ]
