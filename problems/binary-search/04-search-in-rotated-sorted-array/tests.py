import random


def visible():
    return [
        {"in": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}},
        {"in": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}},
        {"in": {"nums": [1], "target": 0}},
    ]


def hidden():
    rng1 = random.Random(3301)
    base1 = sorted(rng1.sample(range(-10000, 10001), 4000))
    k1 = 1739
    rot1 = base1[k1:] + base1[:k1]

    rng2 = random.Random(3302)
    base2 = sorted(rng2.sample(range(-10000, 10001), 4000))
    k2 = 2813
    rot2 = base2[k2:] + base2[:k2]
    present2 = set(base2)
    absent2 = next(x for x in range(-5000, 5000) if x not in present2)

    return [
        {"in": {"nums": [1], "target": 1}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6], "target": 5}},
        {"in": {"nums": [3, 1], "target": 3}},
        {"in": {"nums": [3, 1], "target": 1}},
        {"in": {"nums": [3, 1], "target": 2}},
        {"in": {"nums": [10, -5, -3, 0, 2, 6, 8], "target": -5}},
        {"in": {"nums": [2, 4, 6, 8, 10, 12, -1], "target": -1}},
        {"in": {"nums": [0, 3, 7, 12, -15, -10, -4], "target": 12}},
        {"in": {"nums": [0, 3, 7, 12, -15, -10, -4], "target": -15}},
        {"in": {"nums": rot1, "target": base1[k1 - 1]}},
        {"in": {"nums": rot2, "target": absent2}},
    ]
