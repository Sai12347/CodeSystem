import random


def visible():
    return [
        {"in": {"nums": [10, 2, -10, 5, 20], "k": 2}},
        {"in": {"nums": [-1, -2, -3], "k": 1}},
        {"in": {"nums": [10, -2, -10, -5, 20], "k": 2}},
    ]


def hidden():
    rng = random.Random(1425)
    stress_neg = [rng.randint(-10000, 1000) for _ in range(1800)]
    stress_mix = [rng.randint(-5000, 5000) for _ in range(1500)]
    return [
        {"in": {"nums": [42], "k": 1}},
        {"in": {"nums": [-10000], "k": 1}},
        {"in": {"nums": [-5, -2, -9, -1, -7], "k": 3}},
        {"in": {"nums": [0, 0, 0, 0], "k": 2}},
        {"in": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4], "k": 1}},
        {"in": {"nums": [5, -10, -10, -10, 6, -10, 7], "k": 7}},
        {"in": {"nums": [10, -3, -3, -3, 10], "k": 2}},
        {"in": {"nums": [10, -3, -3, -3, 10], "k": 4}},
        {"in": {"nums": [100, -50, -40, -60, -30, 100], "k": 2}},
        {"in": {"nums": stress_neg, "k": 50}},
        {"in": {"nums": stress_mix, "k": 200}},
    ]
