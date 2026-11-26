import random


def visible():
    return [
        {"in": {"nums": [-1, 0, 1, 2, -1, -4]}},
        {"in": {"nums": [0, 1, 1]}},
        {"in": {"nums": [0, 0, 0]}},
    ]


def hidden():
    rng = random.Random(15)
    med = [rng.randint(-400, 400) for _ in range(120)]
    large = [rng.randint(-100000, 100000) for _ in range(500)]
    return [
        {"in": {"nums": [0, 0, 0, 0, 0]}},
        {"in": {"nums": [1, 2, 3, 4, 5]}},
        {"in": {"nums": [-5, -4, -3, -2, -1]}},
        {"in": {"nums": [-100000, 0, 100000, -100000, 50000, 50000]}},
        {"in": {"nums": [-2, -2, -2, 0, 0, 0, 2, 2, 2, 4, -4]}},
        {"in": {"nums": [-1, -1, 2, -2, 1, 1]}},
        {"in": {"nums": list(range(-10, 11))}},
        {"in": {"nums": list(range(8, -9, -1))}},
        {"in": {"nums": med}},
        {"in": {"nums": large}},
    ]
