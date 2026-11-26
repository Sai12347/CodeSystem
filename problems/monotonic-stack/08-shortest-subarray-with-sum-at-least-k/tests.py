import random


def visible():
    return [
        {"in": {"nums": [1], "k": 1}},
        {"in": {"nums": [1, 2], "k": 4}},
        {"in": {"nums": [2, -1, 2], "k": 3}},
    ]


def hidden():
    rng = random.Random(862)
    stress_osc = [rng.randint(-10000, 12000) for _ in range(1600)]
    stress_big = [100000] * 1200
    return [
        {"in": {"nums": [-5], "k": 1}},
        {"in": {"nums": [10], "k": 5}},
        {"in": {"nums": [84, -37, 32, 40, 95], "k": 167}},
        {"in": {"nums": [-28, 81, -20, 28, -29], "k": 89}},
        {"in": {"nums": [0, 0, 0, 0, 0], "k": 1}},
        {"in": {"nums": [10, -5, 10, -5, 10], "k": 20}},
        {"in": {"nums": [56, -21, 56, 35, -9], "k": 61}},
        {"in": {"nums": [-34, 37, 51, 3, -12, -50, 51, 100, -47, 99, 34, 14, -13, 89, 31, -14, -44, 23, -38, 6], "k": 151}},
        {"in": {"nums": [100000] * 50, "k": 10**9}},
        {"in": {"nums": stress_big, "k": 10**8}},
        {"in": {"nums": stress_osc, "k": 50000}},
    ]
