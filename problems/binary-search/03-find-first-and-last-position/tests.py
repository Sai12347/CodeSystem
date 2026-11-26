import random


def visible():
    return [
        {"in": {"nums": [5, 7, 7, 8, 8, 10], "target": 8}},
        {"in": {"nums": [5, 7, 7, 8, 8, 10], "target": 6}},
        {"in": {"nums": [], "target": 0}},
    ]


def hidden():
    rng1 = random.Random(3401)
    large1 = sorted([rng1.randint(-1000, 1000) for _ in range(3000)] + [42] * 1000)

    rng2 = random.Random(3402)
    large2 = sorted([rng2.randint(-100000, 100000) * 2 for _ in range(4000)])

    return [
        {"in": {"nums": [4], "target": 4}},
        {"in": {"nums": [4], "target": 5}},
        {"in": {"nums": [7, 7, 7, 7, 7, 7], "target": 7}},
        {"in": {"nums": [7, 7, 7, 7], "target": 3}},
        {"in": {"nums": [-1000000000, -1000000000, -5, 0, 10], "target": -1000000000}},
        {"in": {"nums": [-5, 0, 10, 1000000000, 1000000000, 1000000000], "target": 1000000000}},
        {"in": {"nums": [1, 1, 2, 3, 3, 3, 4, 4], "target": 2}},
        {"in": {"nums": [2, 2, 5, 5, 9], "target": 10}},
        {"in": {"nums": [2, 2, 5, 5, 9], "target": 1}},
        {"in": {"nums": large1, "target": 42}},
        {"in": {"nums": large2, "target": 12345}},
    ]
