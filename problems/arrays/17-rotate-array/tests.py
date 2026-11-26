import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}},
        {"in": {"nums": [-1, -100, 3, 99], "k": 2}},
        {"in": {"nums": [1, 2, 3], "k": 4}},
    ]


def hidden():
    rng = random.Random(189)
    arr3k = [rng.randint(-10**9, 10**9) for _ in range(3000)]
    arr4k = [rng.randint(-2**31, 2**31 - 1) for _ in range(4000)]
    return [
        {"in": {"nums": [1, 2, 3, 4], "k": 0}},
        {"in": {"nums": [42], "k": 100000}},
        {"in": {"nums": [10, 20, 30, 40], "k": 4}},
        {"in": {"nums": [1, 2, 3, 4, 5], "k": 15}},
        {"in": {"nums": [1, 2, 3, 4, 5], "k": 4}},
        {"in": {"nums": [1, 2], "k": 99999}},
        {"in": {"nums": [-2147483648, 0, 2147483647, -1], "k": 3}},
        {"in": {"nums": [7, 7, 7, 7, 7], "k": 2}},
        {"in": {"nums": arr3k, "k": 1234}},
        {"in": {"nums": arr4k, "k": 99997}},
    ]
