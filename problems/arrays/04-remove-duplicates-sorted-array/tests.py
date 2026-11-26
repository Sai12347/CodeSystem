import random


def visible():
    return [
        {"in": {"nums": [1, 1, 2]}},
        {"in": {"nums": [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]}},
        {"in": {"nums": [5]}},
    ]


def hidden():
    rng = random.Random(404)
    return [
        {"in": {"nums": [7, 7, 7, 7, 7]}},
        {"in": {"nums": [1, 2, 3, 4, 5]}},
        {"in": {"nums": [-100, -100, -50, 0, 0, 50, 100, 100]}},
        {"in": {"nums": [-10000, 10000]}},
        {"in": {"nums": [0, 0]}},
        {"in": {"nums": [-10000, -10000, -10000, 10000, 10000]}},
        {"in": {"nums": [-5, -5, -4, -3, -3, -3, -1]}},
        {"in": {"nums": [1] * 50 + [2] * 50}},
        {"in": {"nums": sorted(rng.randint(-200, 200) for _ in range(2000))}},
        {"in": {"nums": sorted(rng.randint(-10000, 10000) for _ in range(3000))}},
    ]
