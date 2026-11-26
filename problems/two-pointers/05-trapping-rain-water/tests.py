import random


def visible():
    return [
        {"in": {"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}},
        {"in": {"height": [4, 2, 0, 3, 2, 5]}},
        {"in": {"height": [1, 2, 3, 4]}},
    ]


def hidden():
    rng1 = random.Random(501)
    rand_heights = [rng1.randint(0, 100000) for _ in range(3000)]

    rng2 = random.Random(502)
    valley = [50000 - i * 10 if i < 2500 else (i - 2500) * 10 for i in range(5000)]
    for i in range(1, 4999, 7):
        valley[i] = max(0, valley[i] - rng2.randint(0, 1000))

    return [
        {"in": {"height": [5]}},
        {"in": {"height": [5, 2]}},
        {"in": {"height": [0, 0, 0, 0, 0]}},
        {"in": {"height": [7, 7, 7, 7, 7]}},
        {"in": {"height": [5, 4, 3, 2, 1, 0]}},
        {"in": {"height": [1, 3, 5, 7, 5, 3, 1]}},
        {"in": {"height": [100000, 0, 0, 0, 0, 100000]}},
        {"in": {"height": [5, 2, 2, 4, 1, 1, 3, 0, 6, 1, 2]}},
        {"in": {"height": rand_heights}},
        {"in": {"height": valley}},
    ]
