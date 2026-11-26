import random


def visible():
    return [
        {"in": {"nums": [3, 4, 5, 1, 2]}},
        {"in": {"nums": [4, 5, 6, 7, 0, 1, 2]}},
        {"in": {"nums": [11, 13, 15, 17]}},
    ]


def hidden():
    rng1 = random.Random(1531)
    base1 = sorted(rng1.sample(range(-5000, 5001), 4000))
    k1 = 2719
    rot1 = base1[k1:] + base1[:k1]

    rng2 = random.Random(1532)
    base2 = sorted(rng2.sample(range(-5000, 5001), 4000))

    return [
        {"in": {"nums": [42]}},
        {"in": {"nums": [1, 2]}},
        {"in": {"nums": [2, 1]}},
        {"in": {"nums": [5000, -5000, -2000, 0, 1000]}},
        {"in": {"nums": [-10, -5, 0, 5, 10, -20]}},
        {"in": {"nums": [6, 7, 8, 1, 2, 3, 4]}},
        {"in": {"nums": [-3, -2, -1, -100, -50, -10]}},
        {"in": {"nums": [2, 3, 1]}},
        {"in": {"nums": [3, 1, 2]}},
        {"in": {"nums": rot1}},
        {"in": {"nums": base2}},
    ]
