import random


def visible():
    return [
        {"in": {"nums": [1, -1, 5, -2, 3], "k": 3}},
        {"in": {"nums": [-2, -1, 2, 1], "k": 1}},
        {"in": {"nums": [1, 2, 3], "k": 7}},
    ]


def hidden():
    rng1 = random.Random(3251)
    stress1 = [rng1.randint(-50, 50) for _ in range(2000)]

    rng2 = random.Random(3252)
    stress2 = [rng2.randint(-10000, 10000) for _ in range(2500)]
    target2 = sum(stress2[300:2100])

    return [
        {"in": {"nums": [5], "k": 5}},
        {"in": {"nums": [5], "k": 3}},
        {"in": {"nums": [0, 0, 0, 0, 0], "k": 0}},
        {"in": {"nums": [0, 0, 0, 0], "k": 1}},
        {"in": {"nums": [2, 3, -1, 4, -2], "k": 6}},
        {"in": {"nums": [-5, -2, -3, -1, -4], "k": -6}},
        {"in": {"nums": [1, 0, -1, 1, 0, -1, 1], "k": 1}},
        {"in": {"nums": [-10000] * 100, "k": -1000000}},
        {"in": {"nums": [10000] * 100, "k": -1000000000}},
        {"in": {"nums": stress1, "k": 0}},
        {"in": {"nums": stress2, "k": target2}},
    ]
