import random


def visible():
    return [
        {"in": {"w": [1], "trials": 100}},
        {"in": {"w": [1, 3], "trials": 10000}},
    ]


def hidden():
    rng1 = random.Random(5281)
    stress1 = [rng1.randint(1, 100000) for _ in range(500)]

    rng2 = random.Random(5282)
    stress2 = [rng2.randint(1, 10) for _ in range(750)] + [rng2.randint(1000, 10000) for _ in range(750)]

    return [
        {"in": {"w": [100000], "trials": 500}},
        {"in": {"w": [1, 1, 1, 1], "trials": 10000}},
        {"in": {"w": [90, 5, 5], "trials": 10000}},
        {"in": {"w": [1, 1, 1, 97], "trials": 10000}},
        {"in": {"w": [1, 2, 4, 8, 16], "trials": 10000}},
        {"in": {"w": [1, 100000, 1], "trials": 10000}},
        {"in": {"w": [100000, 100000, 100000, 100000, 100000], "trials": 10000}},
        {"in": {"w": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "trials": 10000}},
        {"in": {"w": stress1, "trials": 10000}},
        {"in": {"w": stress2, "trials": 10000}},
    ]
