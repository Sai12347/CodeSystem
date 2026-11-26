import random


def visible():
    return [
        {"in": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}},
        {"in": {"nums": [1]}},
        {"in": {"nums": [5, 4, -1, 7, 8]}},
    ]


def hidden():
    rng = random.Random(53)
    rand_small = [rng.randint(-100, 100) for _ in range(2000)]
    rand_wide = [rng.randint(-10000, 10000) for _ in range(3000)]
    return [
        {"in": {"nums": [-7]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [-5, -2, -9, -1, -4]}},
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [1, 2, 3, 4, 5]}},
        {"in": {"nums": [10, -20, 3, 4]}},
        {"in": {"nums": [-10, 2, -5, 12]}},
        {"in": {"nums": [100, -101, 100, -99, 100]}},
        {"in": {"nums": rand_small}},
        {"in": {"nums": rand_wide}},
    ]
