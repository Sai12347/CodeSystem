import random


def visible():
    return [
        {"in": {"prices": [7, 1, 5, 3, 6, 4]}},
        {"in": {"prices": [1, 2, 3, 4, 5]}},
        {"in": {"prices": [7, 6, 4, 3, 1]}},
    ]


def hidden():
    rng = random.Random(122)
    rand_3k = [rng.randint(0, 10000) for _ in range(3000)]
    sawtooth = [(i % 20) * 500 for i in range(4000)]
    return [
        {"in": {"prices": [5]}},
        {"in": {"prices": [0, 10000]}},
        {"in": {"prices": [10000, 0]}},
        {"in": {"prices": [3, 3, 3, 3, 3]}},
        {"in": {"prices": [0, 0, 5, 5, 2, 2, 8, 0]}},
        {"in": {"prices": [1, 5, 1, 5, 1, 5, 1, 5]}},
        {"in": {"prices": [5, 2, 2, 2, 7, 7, 7, 1, 1, 9]}},
        {"in": {"prices": list(range(100))}},
        {"in": {"prices": rand_3k}},
        {"in": {"prices": sawtooth}},
    ]
