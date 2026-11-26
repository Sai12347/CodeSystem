import random


def visible():
    return [
        {"in": {"nums": [10, 5, 2, 6], "k": 100}},
        {"in": {"nums": [1, 2, 3], "k": 0}},
        {"in": {"nums": [1, 1, 1], "k": 2}},
    ]


def hidden():
    rng = random.Random(713)
    all_ones = [1] * 2000
    rand_arr = [rng.randint(1, 20) for _ in range(2500)]

    return [
        {"in": {"nums": [1, 1, 1, 1], "k": 1}},
        {"in": {"nums": [5], "k": 6}},
        {"in": {"nums": [5], "k": 5}},
        {"in": {"nums": [10, 2, 2, 5, 4, 4, 4, 3, 7, 7], "k": 289}},
        {"in": {"nums": [10, 20, 30], "k": 10}},
        {"in": {"nums": [1, 2, 1, 2, 1, 2], "k": 1000}},
        {"in": {"nums": [2, 5, 2, 5], "k": 10}},
        {"in": {"nums": [1000, 1000, 1, 999, 1000], "k": 1000000}},
        {"in": {"nums": all_ones, "k": 2}},
        {"in": {"nums": rand_arr, "k": 50000}},
    ]
