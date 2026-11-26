import random


def visible():
    return [
        {"in": {"nums": [1, 3, 5, 6], "target": 5}},
        {"in": {"nums": [1, 3, 5, 6], "target": 2}},
        {"in": {"nums": [1, 3, 5, 6], "target": 7}},
    ]


def hidden():
    large1 = list(range(-8000, 8000, 4))

    rng2 = random.Random(3501)
    large2 = sorted(rng2.sample(range(-10000, 10000), 4000))

    return [
        {"in": {"nums": [1, 3, 5, 6], "target": 0}},
        {"in": {"nums": [1], "target": 0}},
        {"in": {"nums": [1], "target": 1}},
        {"in": {"nums": [1], "target": 2}},
        {"in": {"nums": [-20, -15, -10, -5, -1], "target": -12}},
        {"in": {"nums": [-10000, 0, 10000], "target": -10000}},
        {"in": {"nums": [-10000, 0, 10000], "target": 10000}},
        {"in": {"nums": [1, 10], "target": 5}},
        {"in": {"nums": [-5, -2, 0, 4, 9, 14], "target": -6}},
        {"in": {"nums": large1, "target": 1233}},
        {"in": {"nums": large2, "target": 10000}},
    ]
