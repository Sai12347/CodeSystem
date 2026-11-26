import random


def visible():
    return [
        {"in": {"arr": [3, 2, 4, 1]}},
        {"in": {"arr": [1, 2, 3]}},
        {"in": {"arr": [2, 1]}},
    ]


def hidden():
    rng = random.Random(969)
    stress_rand = list(range(1, 101))
    rng.shuffle(stress_rand)
    stress_rev = list(range(100, 0, -1))

    return [
        {"in": {"arr": [1]}},
        {"in": {"arr": [3, 1, 2]}},
        {"in": {"arr": [5, 4, 3, 2, 1]}},
        {"in": {"arr": [1, 3, 2, 4]}},
        {"in": {"arr": [2, 3, 4, 5, 1]}},
        {"in": {"arr": [5, 1, 2, 3, 4]}},
        {"in": {"arr": [4, 2, 1, 3, 6, 5]}},
        {"in": {"arr": [2, 1, 4, 3, 6, 5, 8, 7]}},
        {"in": {"arr": stress_rev}},
        {"in": {"arr": stress_rand}},
    ]
