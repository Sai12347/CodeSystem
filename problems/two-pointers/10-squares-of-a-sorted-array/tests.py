import random


def visible():
    return [
        {"in": {"nums": [-4, -1, 0, 3, 10]}},
        {"in": {"nums": [-7, -3, 2, 3, 11]}},
        {"in": {"nums": [-5, -3, -2, -1]}},
    ]


def hidden():
    rng = random.Random(977)
    big_rand = sorted(rng.randint(-10000, 10000) for _ in range(2500))
    neg_skew = sorted(rng.randint(-10000, 500) for _ in range(3000))

    return [
        {"in": {"nums": [0]}},
        {"in": {"nums": [-10000]}},
        {"in": {"nums": [10000]}},
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [-3, -3, -3]}},
        {"in": {"nums": [0, 1, 2, 3, 4, 5]}},
        {"in": {"nums": [-5, -2, -1, 1, 2, 5]}},
        {"in": {"nums": [-10000, -4, -4, -1, 0, 0, 1, 4, 4, 10000]}},
        {"in": {"nums": big_rand}},
        {"in": {"nums": neg_skew}},
    ]
