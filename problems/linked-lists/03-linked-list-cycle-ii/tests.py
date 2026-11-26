import random


def visible():
    return [
        {"in": {"head": [3, 2, 0, -4], "pos": 1}},
        {"in": {"head": [1, 2], "pos": 0}},
        {"in": {"head": [1], "pos": -1}},
    ]


def hidden():
    rng = random.Random(142)
    return [
        {"in": {"head": [], "pos": -1}},
        {"in": {"head": [1], "pos": 0}},
        {"in": {"head": [1, 2], "pos": -1}},
        {"in": {"head": [1, 2], "pos": 1}},
        {"in": {"head": [5, 5, 5, 5, 5], "pos": 2}},
        {"in": {"head": [5, 5, 5, 5], "pos": -1}},
        {"in": {"head": list(range(100)), "pos": 95}},
        {"in": {"head": list(range(-50, 50)), "pos": 0}},
        {"in": {"head": list(range(100)), "pos": 99}},
        {"in": {"head": [rng.randint(-100000, 100000) for _ in range(4000)], "pos": 2718}},
        {"in": {"head": [rng.randint(-100000, 100000) for _ in range(4000)], "pos": -1}},
    ]
