import random


def visible():
    return [
        {"in": {"target": 7, "nums": [2, 3, 1, 2, 4, 3]}},
        {"in": {"target": 4, "nums": [1, 4, 4]}},
        {"in": {"target": 11, "nums": [1, 1, 1, 1, 1, 1, 1, 1]}},
    ]


def hidden():
    rng1 = random.Random(209)
    stress1 = [rng1.randint(1, 10000) for _ in range(4000)]

    stress2 = [1] * 3996 + [5000, 5000, 1, 1]

    return [
        {"in": {"target": 5, "nums": [5]}},
        {"in": {"target": 6, "nums": [5]}},
        {"in": {"target": 15, "nums": [1, 2, 3, 4, 5]}},
        {"in": {"target": 16, "nums": [1, 2, 3, 4, 5]}},
        {"in": {"target": 100, "nums": [1, 1, 1, 1, 1, 100]}},
        {"in": {"target": 100, "nums": [100, 1, 1, 1, 1, 1]}},
        {"in": {"target": 15, "nums": [1, 1, 1, 1, 1, 1, 1, 10, 5]}},
        {"in": {"target": 1000000000, "nums": [10000] * 100}},
        {"in": {"target": 50, "nums": list(range(1, 25))}},
        {"in": {"target": 500000, "nums": stress1}},
        {"in": {"target": 10000, "nums": stress2}},
    ]
