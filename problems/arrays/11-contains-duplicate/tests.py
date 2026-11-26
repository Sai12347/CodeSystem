import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 1]}},
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}},
    ]


def hidden():
    rng = random.Random(217)
    unique_large = rng.sample(range(-10**9, 10**9), 4000)
    late_dup = list(unique_large[:-1]) + [unique_large[0]]
    return [
        {"in": {"nums": [42]}},
        {"in": {"nums": [0, 0]}},
        {"in": {"nums": [-1, 1]}},
        {"in": {"nums": [-5, -2, -9, -5]}},
        {"in": {"nums": [-1000000000, 0, 1000000000]}},
        {"in": {"nums": [1000000000, -1000000000, 1000000000]}},
        {"in": {"nums": list(range(-50, 50))}},
        {"in": {"nums": list(range(50, 0, -1)) + [50]}},
        {"in": {"nums": unique_large}},
        {"in": {"nums": late_dup}},
    ]
