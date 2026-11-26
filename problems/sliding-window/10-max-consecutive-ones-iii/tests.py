import random


def visible():
    return [
        {"in": {"nums": [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], "k": 2}},
        {"in": {"nums": [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], "k": 3}},
        {"in": {"nums": [0, 0, 0, 0], "k": 0}},
    ]


def hidden():
    rng1 = random.Random(1004)
    big_rand = [rng1.randint(0, 1) for _ in range(2000)]

    rng2 = random.Random(10040)
    sparse_zeros = [0 if rng2.random() < 0.08 else 1 for _ in range(2500)]

    return [
        {"in": {"nums": [1], "k": 0}},
        {"in": {"nums": [0], "k": 1}},
        {"in": {"nums": [0], "k": 0}},
        {"in": {"nums": [1, 1, 1, 1, 1], "k": 0}},
        {"in": {"nums": [0, 0, 0, 0, 0], "k": 5}},
        {"in": {"nums": [1, 0, 1, 1, 0, 1, 1, 1, 0, 1], "k": 0}},
        {"in": {"nums": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], "k": 2}},
        {"in": {"nums": [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1], "k": 1}},
        {"in": {"nums": big_rand, "k": 150}},
        {"in": {"nums": sparse_zeros, "k": 20}},
    ]
