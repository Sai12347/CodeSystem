import random


def visible():
    return [
        {"in": {"heights": [10, 6, 8, 5, 11, 9]}},
        {"in": {"heights": [5, 1, 2, 3, 10]}},
        {"in": {"heights": [1, 2, 3, 4]}},
    ]


def hidden():
    rng = random.Random(1944)
    stress_perm = rng.sample(range(1, 100001), 2000)
    stress_tall_left = [100000] + list(range(1, 1500))
    return [
        {"in": {"heights": [100]}},
        {"in": {"heights": [1, 2]}},
        {"in": {"heights": [2, 1]}},
        {"in": {"heights": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"heights": [100, 1, 2, 3, 4, 5, 6, 7]}},
        {"in": {"heights": [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]}},
        {"in": {"heights": [50, 10, 20, 30, 40, 60]}},
        {"in": {"heights": [100000, 50000, 1, 25000, 75000, 99999]}},
        {"in": {"heights": [4, 3, 2, 1, 5, 6, 7, 8]}},
        {"in": {"heights": stress_tall_left}},
        {"in": {"heights": stress_perm}},
    ]
