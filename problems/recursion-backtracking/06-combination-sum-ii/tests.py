import random


def visible():
    return [
        {"in": {"candidates": [10, 1, 2, 7, 6, 1, 5], "target": 8}},
        {"in": {"candidates": [2, 5, 2, 1, 2], "target": 5}},
        {"in": {"candidates": [3, 4, 5], "target": 2}},
    ]


def hidden():
    rng = random.Random(40)
    rand_cands = [rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 40, 50]) for _ in range(40)]
    return [
        {"in": {"candidates": [7], "target": 7}},
        {"in": {"candidates": [7], "target": 6}},
        {"in": {"candidates": [2, 2, 2, 2, 2], "target": 6}},
        {"in": {"candidates": [2, 2, 2], "target": 8}},
        {"in": {"candidates": [1] * 100, "target": 30}},
        {"in": {"candidates": [1] * 25 + [2] * 25, "target": 27}},
        {"in": {"candidates": [50, 40, 31, 15, 15, 10, 5, 5, 5], "target": 30}},
        {"in": {"candidates": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 5, 5, 2, 2], "target": 12}},
        {"in": {"candidates": [2, 4, 6, 8, 2, 4, 6, 8, 10, 12], "target": 21}},
        {"in": {"candidates": rand_cands, "target": 25}},
    ]
