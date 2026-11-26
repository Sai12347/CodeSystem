import random


def visible():
    return [
        {"in": {"weights": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "days": 5}},
        {"in": {"weights": [3, 2, 2, 4, 1, 4], "days": 3}},
        {"in": {"weights": [1, 2, 3, 1, 1], "days": 4}},
    ]


def hidden():
    rng1 = random.Random(1011)
    stress1 = [rng1.randint(1, 500) for _ in range(2000)]

    rng2 = random.Random(101102)
    stress2 = [rng2.randint(1, 500) for _ in range(4000)]

    return [
        {"in": {"weights": [42], "days": 1}},
        {"in": {"weights": [10, 20, 30, 40], "days": 1}},
        {"in": {"weights": [5, 100, 3, 50, 2], "days": 5}},
        {"in": {"weights": [10, 10, 10, 10, 10], "days": 2}},
        {"in": {"weights": [1, 1, 1, 1, 500], "days": 2}},
        {"in": {"weights": [10, 10, 500, 10, 10], "days": 3}},
        {"in": {"weights": [50, 45, 40, 35, 30, 25, 20, 15, 10, 5], "days": 4}},
        {"in": {"weights": [500, 1, 500, 1, 500, 1, 500], "days": 4}},
        {"in": {"weights": stress1, "days": 50}},
        {"in": {"weights": stress2, "days": 250}},
    ]
