import random


def visible():
    return [
        {"in": {"board": [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]}},
        {"in": {"board": [[1, 1], [1, 0]]}},
    ]


def hidden():
    rng = random.Random(28905)
    blinker = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    glider = [
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    checker = [[(r + c) % 2 for c in range(6)] for r in range(6)]
    stress = [[rng.randint(0, 1) for _ in range(40)] for _ in range(40)]
    return [
        {"in": {"board": [[1]]}},
        {"in": {"board": [[0]]}},
        {"in": {"board": [[1, 1, 1, 0, 1, 1]]}},
        {"in": {"board": [[1], [1], [1], [0], [1]]}},
        {"in": {"board": [[0] * 4 for _ in range(4)]}},
        {"in": {"board": [[1] * 4 for _ in range(4)]}},
        {"in": {"board": blinker}},
        {"in": {"board": glider}},
        {"in": {"board": checker}},
        {"in": {"board": stress}},
    ]
