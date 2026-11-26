import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 4, 5]}},
        {"in": {"nums": [10, -2, 7, 0]}},
        {"in": {"nums": [42]}},
    ]


def hidden():
    rng = random.Random(202)
    return [
        {"in": {"nums": []}},
        {"in": {"nums": [1, 2]}},
        {"in": {"nums": [5, 5, 5, 5]}},
        {"in": {"nums": [1, 2, 3, 2, 1]}},
        {"in": {"nums": [-1000000000, 0, 1000000000]}},
        {"in": {"nums": list(range(1, 26))}},
        {"in": {"nums": list(range(25, 0, -1))}},
        {"in": {"nums": [-1, -2, -3, -4, -5, -6]}},
        {"in": {"nums": [rng.randint(-10**9, 10**9) for _ in range(2000)]}},
        {"in": {"nums": [rng.randint(-1000, 1000) for _ in range(3001)]}},
    ]
