import random


def visible():
    return [
        {"in": {"nums": [12, 4, 19, 8, 23, 15, 42]}},
        {"in": {"nums": [-7]}},
        {"in": {"nums": [-5, -1, -9, -3]}},
    ]


def hidden():
    rng = random.Random(101)
    return [
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [5, 2]}},
        {"in": {"nums": [-1000000000, 1000000000]}},
        {"in": {"nums": [1000000000, 1000000000]}},
        {"in": {"nums": [-1000000000, -1000000000]}},
        {"in": {"nums": list(range(1, 51))}},
        {"in": {"nums": list(range(50, 0, -1))}},
        {"in": {"nums": [7, -3, 7, -3, 0, 7, -3]}},
        {"in": {"nums": [rng.randint(-10**9, 10**9) for _ in range(2000)]}},
        {"in": {"nums": [rng.randint(-50, 50) for _ in range(3000)]}},
    ]
