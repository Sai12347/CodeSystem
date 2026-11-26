import random


def visible():
    return [
        {"in": {"nums": [4, 5, 0, -2, -3, 1], "k": 5}},
        {"in": {"nums": [5], "k": 9}},
        {"in": {"nums": [-1, 2, 9], "k": 2}},
    ]


def hidden():
    rng = random.Random(974)
    big_random = [rng.randint(-10000, 10000) for _ in range(1500)]
    big_zeros = [0] * 1000
    neg_chain = [-7] * 500
    return [
        {"in": {"nums": [0], "k": 2}},
        {"in": {"nums": [-5], "k": 5}},
        {"in": {"nums": [-1, -2, -3, -4], "k": 3}},
        {"in": {"nums": [2, -2, 2, -4], "k": 6}},
        {"in": {"nums": [0, 0, 0, 0], "k": 10000}},
        {"in": {"nums": [1, 1, 1, 1, 1], "k": 10}},
        {"in": {"nums": [-10000, 10000, -10000, 10000], "k": 10000}},
        {"in": {"nums": [7, -5, 5, -8, -6, 6, -4, 7, -8, -7], "k": 7}},
        {"in": {"nums": neg_chain, "k": 7}},
        {"in": {"nums": big_zeros, "k": 37}},
        {"in": {"nums": big_random, "k": 97}},
    ]
