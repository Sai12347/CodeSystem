import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [1, 1, 1, 1, 1]}},
        {"in": {"nums": [3, 1, 2, 10, 1]}},
    ]


def hidden():
    rng = random.Random(1480)
    big_random = [rng.randint(-10**6, 10**6) for _ in range(1000)]
    max_vals = [10**6] * 1000
    min_vals = [-10**6] * 1000
    alternating = [10**6 if i % 2 == 0 else -10**6 for i in range(500)]
    return [
        {"in": {"nums": [0]}},
        {"in": {"nums": [-42]}},
        {"in": {"nums": [0, 0, 0, 0, 0]}},
        {"in": {"nums": [-5, -4, -3, -2, -1]}},
        {"in": {"nums": [10, -10, 10, -10, 10, -10]}},
        {"in": {"nums": [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]}},
        {"in": {"nums": [-1000000, 1000000, -1000000, 1000000]}},
        {"in": {"nums": alternating}},
        {"in": {"nums": max_vals}},
        {"in": {"nums": min_vals}},
        {"in": {"nums": big_random}},
    ]
