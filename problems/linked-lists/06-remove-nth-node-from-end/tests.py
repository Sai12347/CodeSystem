import random


def visible():
    return [
        {"in": {"head": [1, 2, 3, 4, 5], "n": 2}},
        {"in": {"head": [1], "n": 1}},
        {"in": {"head": [1, 2], "n": 1}},
    ]


def hidden():
    rng = random.Random(19)
    return [
        {"in": {"head": [1, 2], "n": 2}},
        {"in": {"head": [10, 20, 30, 40, 50], "n": 5}},
        {"in": {"head": [10, 20, 30, 40, 50], "n": 1}},
        {"in": {"head": [1, 2, 3, 4, 5], "n": 3}},
        {"in": {"head": [7, 7, 7, 7], "n": 2}},
        {"in": {"head": [-10000, -5, 0, 5, 10000], "n": 4}},
        {"in": {"head": [9, 7, 5, 3, 1], "n": 3}},
        {"in": {"head": list(range(3000)), "n": 3000}},
        {"in": {"head": list(range(3000)), "n": 1}},
        {"in": {"head": [rng.randint(-10000, 10000) for _ in range(4000)], "n": 2001}},
    ]
