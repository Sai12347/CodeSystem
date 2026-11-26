import random


def visible():
    return [
        {"in": {"nums": [-1, -2, -3, -4, 3, 2, 1]}},
        {"in": {"nums": [1, 5, 0, 2, -3]}},
        {"in": {"nums": [-1, 1, -1, 1, -1]}},
    ]


def hidden():
    rng = random.Random(1822)
    nonzero_choices = [x for x in range(-100, 101) if x != 0]
    large_nz = [rng.choice(nonzero_choices) for _ in range(1000)]
    large_zero = [rng.choice(nonzero_choices) for _ in range(1000)]
    large_zero[900] = 0
    return [
        {"in": {"nums": [7]}},
        {"in": {"nums": [-100]}},
        {"in": {"nums": [0]}},
        {"in": {"nums": [100] * 50 + [0]}},
        {"in": {"nums": [100] * 100}},
        {"in": {"nums": [-100] * 99}},
        {"in": {"nums": [-100] * 100}},
        {"in": {"nums": [-1, 1] * 25}},
        {"in": {"nums": large_nz}},
        {"in": {"nums": large_zero}},
    ]
