import random


def visible():
    return [
        {"in": {"head": [1, 2, 3, 4]}},
        {"in": {"head": [1, 2, 3, 4, 5]}},
        {"in": {"head": [1, 2, 3]}},
    ]


def hidden():
    rng = random.Random(143)
    return [
        {"in": {"head": [1]}},
        {"in": {"head": [1, 2]}},
        {"in": {"head": [1, 2, 3, 4, 5, 6]}},
        {"in": {"head": [5, 5, 5, 5, 5]}},
        {"in": {"head": [1, 2, 3, 2, 1]}},
        {"in": {"head": [-10000, -1, 0, 1, 10000, 50]}},
        {"in": {"head": [10, 9, 8, 7, 6, 5, 4]}},
        {"in": {"head": [1, 1, 2, 2, 3, 3, 4, 4]}},
        {"in": {"head": list(range(1, 4001))}},
        {"in": {"head": [rng.randint(-10000, 10000) for _ in range(4001)]}},
    ]
