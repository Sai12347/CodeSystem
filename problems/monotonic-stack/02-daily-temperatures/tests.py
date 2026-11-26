import random


def visible():
    return [
        {"in": {"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]}},
        {"in": {"temperatures": [30, 40, 50, 60]}},
        {"in": {"temperatures": [30, 60, 90]}},
    ]


def hidden():
    rng = random.Random(739)
    stress_rand = [rng.randint(30, 100) for _ in range(2000)]
    stress_wait = [99 - (i % 70) for i in range(1499)] + [100]
    return [
        {"in": {"temperatures": [70]}},
        {"in": {"temperatures": [50] * 10}},
        {"in": {"temperatures": [100, 90, 80, 70, 60, 50, 40, 30]}},
        {"in": {"temperatures": [30, 30, 100, 30, 100]}},
        {"in": {"temperatures": [50, 50, 50, 51]}},
        {"in": {"temperatures": [30, 100, 30, 100, 30, 100]}},
        {"in": {"temperatures": [100, 30, 31, 32, 33, 99]}},
        {"in": {"temperatures": [80, 70, 60, 70, 80]}},
        {"in": {"temperatures": [35, 34, 33, 32, 31, 30, 36]}},
        {"in": {"temperatures": stress_wait}},
        {"in": {"temperatures": stress_rand}},
    ]
