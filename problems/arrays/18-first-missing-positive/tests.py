import random


def visible():
    return [
        {"in": {"nums": [1, 2, 0]}},
        {"in": {"nums": [3, 4, -1, 1]}},
        {"in": {"nums": [7, 8, 9, 11, 12]}},
    ]


def hidden():
    rng = random.Random(41)
    almost_full = list(range(1, 4001))
    almost_full[2345] = -5
    rng.shuffle(almost_full)

    rand_mix = [rng.randint(-500, 5000) for _ in range(4000)]
    return [
        {"in": {"nums": [1]}},
        {"in": {"nums": [2]}},
        {"in": {"nums": [-5]}},
        {"in": {"nums": [-2147483648, -1, 0, -100]}},
        {"in": {"nums": [-2147483648, 2147483647, 1, 2]}},
        {"in": {"nums": [1, 1, 2, 2, 3, 3]}},
        {"in": {"nums": list(range(20, 0, -1))}},
        {"in": {"nums": [2, 2, 1, 4, 5, 1, 4]}},
        {"in": {"nums": almost_full}},
        {"in": {"nums": rand_mix}},
    ]
