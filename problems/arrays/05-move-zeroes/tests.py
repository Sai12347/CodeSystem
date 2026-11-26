import random


def visible():
    return [
        {"in": {"nums": [0, 1, 0, 3, 12]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [1, 2, 3]}},
    ]


def hidden():
    rng = random.Random(505)
    s1 = [0 if rng.random() < 0.5 else rng.randint(-1000, 1000) for _ in range(2000)]
    s2 = [0 if rng.random() < 0.1 else rng.randint(-10**9, 10**9) for _ in range(3000)]
    return [
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [5]}},
        {"in": {"nums": [0, 0, 1]}},
        {"in": {"nums": [1, 0, 0]}},
        {"in": {"nums": [0, -1, 0, -2, 0, 3]}},
        {"in": {"nums": [-2147483648, 0, 2147483647, 0]}},
        {"in": {"nums": [0, 1, 0, 1, 0, 1, 0, 1]}},
        {"in": {"nums": [4, 2, 4, 0, 0, 3, 0, 5, 1, 0]}},
        {"in": {"nums": s1}},
        {"in": {"nums": s2}},
    ]
