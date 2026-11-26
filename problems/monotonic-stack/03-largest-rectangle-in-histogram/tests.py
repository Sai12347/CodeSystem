import random


def visible():
    return [
        {"in": {"heights": [2, 1, 5, 6, 2, 3]}},
        {"in": {"heights": [2, 4]}},
        {"in": {"heights": [0, 9]}},
    ]


def hidden():
    rng = random.Random(84)
    stress_rand = [rng.randint(0, 10000) for _ in range(2000)]
    stress_flat = [10000] * 1500
    return [
        {"in": {"heights": [0]}},
        {"in": {"heights": [10000]}},
        {"in": {"heights": [0, 0, 0, 0, 0]}},
        {"in": {"heights": [5] * 20}},
        {"in": {"heights": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"heights": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"heights": [4, 2, 0, 3, 2, 5]}},
        {"in": {"heights": [1] * 10 + [10] + [1] * 10}},
        {"in": {"heights": [1, 2, 3, 4, 5, 4, 3, 2, 1]}},
        {"in": {"heights": [6, 2, 5, 4, 5, 1, 6]}},
        {"in": {"heights": stress_flat}},
        {"in": {"heights": stress_rand}},
    ]
