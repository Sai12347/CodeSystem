import random


def visible():
    return [
        {"in": {"people": [1, 2], "limit": 3}},
        {"in": {"people": [3, 2, 2, 1], "limit": 3}},
        {"in": {"people": [3, 5, 3, 4], "limit": 5}},
    ]


def hidden():
    rng1 = random.Random(801)
    stress1 = [rng1.randint(1, 1000) for _ in range(2000)]

    rng2 = random.Random(802)
    stress2 = [rng2.randint(1, 30000) for _ in range(4000)]

    return [
        {"in": {"people": [1], "limit": 1}},
        {"in": {"people": [30000], "limit": 30000}},
        {"in": {"people": [1, 1, 1, 1, 1], "limit": 10}},
        {"in": {"people": [5, 5, 5, 5, 5, 5], "limit": 10}},
        {"in": {"people": [8, 8, 8, 8], "limit": 8}},
        {"in": {"people": [1, 2, 4, 5], "limit": 6}},
        {"in": {"people": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "limit": 10}},
        {"in": {"people": [9, 9, 7, 5, 5, 3, 2, 1, 1], "limit": 10}},
        {"in": {"people": stress1, "limit": 1000}},
        {"in": {"people": stress2, "limit": 30000}},
    ]
