import random


def visible():
    return [
        {"in": {"digits": [1, 2, 3]}},
        {"in": {"digits": [4, 3, 2, 1]}},
        {"in": {"digits": [9]}},
    ]


def hidden():
    rng = random.Random(707)
    big_rand = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(999)]
    return [
        {"in": {"digits": [0]}},
        {"in": {"digits": [9, 9]}},
        {"in": {"digits": [9, 9, 9, 9]}},
        {"in": {"digits": [1, 9, 9]}},
        {"in": {"digits": [8, 9, 9, 9]}},
        {"in": {"digits": [1, 0, 0, 0]}},
        {"in": {"digits": [9, 8, 9]}},
        {"in": {"digits": [9] * 20}},
        {"in": {"digits": [9] * 500}},
        {"in": {"digits": big_rand}},
    ]
