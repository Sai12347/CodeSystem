import random


def visible():
    return [
        {"in": {"head": [1, 2, 3, 4, 5]}},
        {"in": {"head": [1, 2]}},
        {"in": {"head": []}},
    ]


def hidden():
    rng = random.Random(206)
    return [
        {"in": {"head": [42]}},
        {"in": {"head": [-5000]}},
        {"in": {"head": [7, 7, 7, 7, 7]}},
        {"in": {"head": [1, 2, 3, 2, 1]}},
        {"in": {"head": [-5000, -1, 0, 1, 5000]}},
        {"in": {"head": [10, 8, 6, 4, 2, 0, -2]}},
        {"in": {"head": [1, 1, 2, 2, 3, 3]}},
        {"in": {"head": [1, -1, 2, -2, 3, -3, 4, -4]}},
        {"in": {"head": list(range(-250, 250))}},
        {"in": {"head": [rng.randint(-5000, 5000) for _ in range(5000)]}},
    ]
