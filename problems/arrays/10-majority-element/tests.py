import random


def visible():
    return [
        {"in": {"nums": [3, 2, 3]}},
        {"in": {"nums": [2, 2, 1, 1, 1, 2, 2]}},
        {"in": {"nums": [7]}},
    ]


def hidden():
    rng = random.Random(1010)
    s1 = [42] * 1001 + [rng.randint(-1000, 1000) for _ in range(1000)]
    rng.shuffle(s1)
    s2 = [-999999999] * 1501 + [rng.randint(-10**9, 10**9) for _ in range(1499)]
    rng.shuffle(s2)
    return [
        {"in": {"nums": [5, 5, 5, 5, 5]}},
        {"in": {"nums": [-1, -1, 2]}},
        {"in": {"nums": [0, 0, 1, 0, 2, 0]}},
        {"in": {"nums": [1, 2, 1, 2, 1]}},
        {"in": {"nums": [1, 1, 1, 2, 3]}},
        {"in": {"nums": [2, 3, 1, 1, 1]}},
        {"in": {"nums": [-1000000000, 1000000000, -1000000000]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 5, 5, 5, 5, 5]}},
        {"in": {"nums": s1}},
        {"in": {"nums": s2}},
    ]
