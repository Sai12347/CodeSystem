import random


def visible():
    return [
        {"in": {"nums": [1, 2, 1]}},
        {"in": {"nums": [1, 2, 3, 4, 3]}},
        {"in": {"nums": [5, 4, 3, 2, 1]}},
    ]


def hidden():
    rng = random.Random(503)
    stress_rand = [rng.randint(-10**9, 10**9) for _ in range(1500)]
    stress_desc = list(range(1000, 0, -1))
    return [
        {"in": {"nums": [42]}},
        {"in": {"nums": [7, 7, 7, 7, 7]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6]}},
        {"in": {"nums": [-1, -2, -3, -4, -5]}},
        {"in": {"nums": [-10**9, 0, 10**9, -10**9, 10**9]}},
        {"in": {"nums": [10, 1, 2, 3, 4]}},
        {"in": {"nums": [3, 3, 1, 2, 3, 4, 3]}},
        {"in": {"nums": [5, 1, 5, 1, 5]}},
        {"in": {"nums": [2, 1]}},
        {"in": {"nums": stress_desc}},
        {"in": {"nums": stress_rand}},
    ]
