import random


def visible():
    return [
        {"in": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}},
        {"in": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}},
        {"in": {"nums": [5], "target": 5}},
    ]


def hidden():
    rng1 = random.Random(7041)
    large1 = sorted(rng1.sample(range(-9999, 10000), 4000))

    rng2 = random.Random(7042)
    large2 = sorted(rng2.sample(range(-9999, 10000), 4000))
    present2 = set(large2)
    absent2 = next(x for x in range(100, 9999) if x not in present2)

    return [
        {"in": {"nums": [5], "target": -5}},
        {"in": {"nums": [-10, -3, 0, 4, 8], "target": -10}},
        {"in": {"nums": [-10, -3, 0, 4, 8], "target": 8}},
        {"in": {"nums": [1, 3, 5, 7], "target": 0}},
        {"in": {"nums": [1, 3, 5, 7], "target": 10}},
        {"in": {"nums": [2, 5], "target": 5}},
        {"in": {"nums": [2, 5], "target": 3}},
        {"in": {"nums": [-9999, -5000, 0, 5000, 9999], "target": -9999}},
        {"in": {"nums": [-8, -4, -1, 0, 3, 7, 11, 15], "target": 0}},
        {"in": {"nums": large1, "target": large1[3456]}},
        {"in": {"nums": large2, "target": absent2}},
    ]
