import random


def visible():
    return [
        {"in": {"nums": [3, 2, 1, 5, 6, 4], "k": 2}},
        {"in": {"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6], "k": 4}},
        {"in": {"nums": [-7], "k": 1}},
    ]


def hidden():
    rng1 = random.Random(21501)
    stress1 = [rng1.randint(-10000, 10000) for _ in range(3000)]

    rng2 = random.Random(21502)
    # Many duplicates (adversarial for naive quickselect)
    stress2 = [rng2.choice([-100, 0, 42, 42, 42, 9999]) for _ in range(2500)]

    return [
        {"in": {"nums": [7, 7, 7, 7, 7], "k": 3}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 1}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 7}},
        {"in": {"nums": [10, 9, 8, 7, 6, 5, 4], "k": 5}},
        {"in": {"nums": [-10000, -5000, -1, -2, -10000, -3], "k": 4}},
        {"in": {"nums": [-10000, 10000, -10000, 10000, 0], "k": 2}},
        {"in": {"nums": [-10000, 10000, -10000, 10000, 0], "k": 3}},
        {"in": {"nums": [2, 1], "k": 2}},
        {"in": {"nums": stress1, "k": 1234}},
        {"in": {"nums": stress2, "k": 1250}},
    ]
