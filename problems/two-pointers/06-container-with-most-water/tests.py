import random


def visible():
    return [
        {"in": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}},
        {"in": {"height": [1, 1]}},
        {"in": {"height": [4, 3, 2, 1, 4]}},
    ]


def hidden():
    rng1 = random.Random(601)
    rand1 = [rng1.randint(0, 10000) for _ in range(2000)]

    rng2 = random.Random(602)
    rand2 = [rng2.randint(0, 500) for _ in range(3000)]
    rand2[1200] = 10000
    rand2[1800] = 10000

    return [
        {"in": {"height": [0, 10000]}},
        {"in": {"height": [0, 0, 0, 0, 0]}},
        {"in": {"height": [5, 5, 5, 5, 5, 5]}},
        {"in": {"height": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"height": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"height": [1, 2, 1, 10000, 10000, 1, 2, 1]}},
        {"in": {"height": [2, 3, 10, 5, 7, 8, 9]}},
        {"in": {"height": [10000] + [1] * 100 + [10000]}},
        {"in": {"height": rand1}},
        {"in": {"height": rand2}},
    ]
