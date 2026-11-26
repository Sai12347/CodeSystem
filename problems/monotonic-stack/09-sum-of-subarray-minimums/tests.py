import random


def visible():
    return [
        {"in": {"arr": [3, 1, 2, 4]}},
        {"in": {"arr": [11, 81, 94, 43, 3]}},
        {"in": {"arr": [1, 1, 1]}},
    ]


def hidden():
    rng = random.Random(907)
    stress_dups = [rng.randint(1, 50) for _ in range(1800)]
    stress_full = [rng.randint(1, 30000) for _ in range(1500)]
    return [
        {"in": {"arr": [1]}},
        {"in": {"arr": [30000]}},
        {"in": {"arr": [5] * 10}},
        {"in": {"arr": [1, 2, 3, 4, 5, 6, 7]}},
        {"in": {"arr": [7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"arr": [2, 1, 2, 1, 2, 1]}},
        {"in": {"arr": [1, 3, 3, 3, 1]}},
        {"in": {"arr": [71, 55, 82, 55]}},
        {"in": {"arr": [30000] * 1500}},
        {"in": {"arr": stress_dups}},
        {"in": {"arr": stress_full}},
    ]
