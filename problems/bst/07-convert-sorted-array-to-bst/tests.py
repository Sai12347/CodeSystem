import random


def visible():
    return [
        {"in": {"nums": [-10, -3, 0, 5, 9]}},
        {"in": {"nums": [1, 3]}},
        {"in": {"nums": [0]}},
    ]


def hidden():
    rng1 = random.Random(1081)
    med = sorted(rng1.sample(range(-10000, 10001), 500))

    rng2 = random.Random(1082)
    large = sorted(rng2.sample(range(-10000, 10001), 3000))

    return [
        {"in": {"nums": [-5, -1]}},
        {"in": {"nums": [1, 2, 3]}},
        {"in": {"nums": [-100, -50, 50, 100]}},
        {"in": {"nums": [-3, -2, -1, 0, 1, 2, 3]}},
        {"in": {"nums": [-10000, -9999, -1, 0, 1, 2, 9999, 10000]}},
        {"in": {"nums": list(range(1, 16))}},
        {"in": {"nums": list(range(-8, 8))}},
        {"in": {"nums": [-10000, 10000]}},
        {"in": {"nums": med}},
        {"in": {"nums": large}},
    ]
