import random


def visible():
    return [
        {"in": {"nums": [3, 2, 2, 3], "val": 3}},
        {"in": {"nums": [0, 1, 2, 2, 3, 0, 4, 2], "val": 2}},
        {"in": {"nums": [], "val": 0}},
    ]


def hidden():
    rng1 = random.Random(401)
    dense = [rng1.choice([5, 5, 1, 2, 3, 4]) for _ in range(2000)]

    rng2 = random.Random(402)
    sparse = [rng2.randint(-100, 100) for _ in range(4000)]

    return [
        {"in": {"nums": [5], "val": 5}},
        {"in": {"nums": [5], "val": 3}},
        {"in": {"nums": [7, 7, 7, 7, 7], "val": 7}},
        {"in": {"nums": [1, 2, 3, 4, 5], "val": 9}},
        {"in": {"nums": [4, 1, 2, 3, 4], "val": 4}},
        {"in": {"nums": [0, 1, 0, 2, 0, 3, 0], "val": 0}},
        {"in": {"nums": [-10000, 0, 10000, -10000, 5], "val": -10000}},
        {"in": {"nums": [9, 9, 8, 7, 7, 7, 6, 5], "val": 7}},
        {"in": {"nums": dense, "val": 5}},
        {"in": {"nums": sparse, "val": 0}},
    ]
