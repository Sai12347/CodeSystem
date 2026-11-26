import random


def visible():
    return [
        {"in": {"arr": [1, 2, 3, 4, 5], "k": 4, "x": 3}},
        {"in": {"arr": [1, 2, 3, 4, 5], "k": 4, "x": -1}},
        {"in": {"arr": [1, 1, 2, 3, 4, 5], "k": 4, "x": 3}},
    ]


def hidden():
    rng1 = random.Random(658)
    stress1 = sorted(rng1.randint(-10000, 10000) for _ in range(3000))

    rng2 = random.Random(65802)
    stress2 = sorted(rng2.randint(-10000, 10000) for _ in range(5000))

    return [
        {"in": {"arr": [5], "k": 1, "x": 100}},
        {"in": {"arr": [-5, -2, 0, 3, 7], "k": 5, "x": 1}},
        {"in": {"arr": [1, 3, 5, 7, 9], "k": 2, "x": 100}},
        {"in": {"arr": [-100, -50, -10, 0, 10], "k": 3, "x": -500}},
        {"in": {"arr": [0, 2, 4, 6, 8], "k": 3, "x": 3}},
        {"in": {"arr": [1, 1, 2, 2, 2, 2, 2, 3, 3], "k": 3, "x": 3}},
        {"in": {"arr": [1, 1, 2, 2, 2, 2, 2, 3, 3], "k": 3, "x": 1}},
        {"in": {"arr": [4, 4, 4, 4, 4, 4], "k": 3, "x": 10}},
        {"in": {"arr": stress1, "k": 500, "x": 1234}},
        {"in": {"arr": stress2, "k": 1, "x": -4321}},
    ]
