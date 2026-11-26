import random


def visible():
    return [
        {"in": {"nums": [1, 1, 2, 1, 1], "k": 3}},
        {"in": {"nums": [2, 4, 6], "k": 1}},
        {"in": {"nums": [2, 2, 2, 1, 2, 2, 1, 2, 2, 2], "k": 2}},
    ]


def hidden():
    rng1 = random.Random(1248)
    big1 = [rng1.randint(1, 100000) for _ in range(1500)]

    rng2 = random.Random(12480)
    big2 = [
        rng2.randint(0, 49999) * 2 + (1 if rng2.random() < 0.06 else 2)
        for _ in range(1500)
    ]

    return [
        {"in": {"nums": [1], "k": 1}},
        {"in": {"nums": [2], "k": 1}},
        {"in": {"nums": [1, 3, 5, 7, 9], "k": 1}},
        {"in": {"nums": [1, 3, 5, 7, 9], "k": 5}},
        {"in": {"nums": [1, 2, 3, 4, 5], "k": 4}},
        {"in": {"nums": [100000, 99999, 100000, 99999, 100000], "k": 1}},
        {"in": {"nums": [2, 1, 2, 1, 2, 1, 2], "k": 2}},
        {"in": {"nums": [4, 4, 1, 3, 5, 6, 7, 8, 8], "k": 3}},
        {"in": {"nums": big1, "k": 25}},
        {"in": {"nums": big2, "k": 10}},
    ]
