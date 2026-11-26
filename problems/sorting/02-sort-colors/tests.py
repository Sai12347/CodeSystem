import random


def visible():
    return [
        {"in": {"nums": [2, 0, 2, 1, 1, 0]}},
        {"in": {"nums": [2, 0, 1]}},
        {"in": {"nums": [0]}},
    ]


def hidden():
    rng1 = random.Random(75)
    rng2 = random.Random(76)
    return [
        {"in": {"nums": [1]}},
        {"in": {"nums": [2]}},
        {"in": {"nums": [1, 0]}},
        {"in": {"nums": [2, 2, 2, 2, 2]}},
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [0, 0, 1, 1, 2, 2]}},
        {"in": {"nums": [2, 2, 1, 1, 0, 0]}},
        {"in": {"nums": [2, 0, 2, 0, 2, 0, 2, 0]}},
        {"in": {"nums": [1, 2, 0, 1, 2, 0, 1, 2, 0]}},
        {"in": {"nums": [rng1.randint(0, 2) for _ in range(300)]}},
        {"in": {"nums": [rng2.choice([0, 2]) for _ in range(250)]}},
    ]
