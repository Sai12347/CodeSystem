import random


def visible():
    return [
        {"in": {"nums": [2, 7, 11, 15], "target": 9}},
        {"in": {"nums": [3, 2, 4], "target": 6}},
        {"in": {"nums": [3, 3], "target": 6}},
    ]


def hidden():
    rng = random.Random(303)

    # Stress 1: distractors in [-10000, 10000], unique pair sums to 900_000_000
    s1 = [rng.randint(-10000, 10000) for _ in range(1998)]
    s1.insert(450, 400000000)
    s1.insert(1850, 500000000)

    # Stress 2: distractors in [1, 100000], unique pair sums to -700_000_000
    s2 = [rng.randint(1, 100000) for _ in range(2998)]
    s2.insert(2997, -300000000)
    s2.insert(2999, -400000000)

    return [
        {"in": {"nums": [-3, 4, 3, 90], "target": 0}},
        {"in": {"nums": [-10, -20, -30, -40, -50], "target": -90}},
        {"in": {"nums": [0, 4, 3, 0], "target": 0}},
        {"in": {"nums": [1000000000, -1000000000, 5, 7], "target": 0}},
        {"in": {"nums": [500000000, 500000000, 1, 2, 3], "target": 1000000000}},
        {"in": {"nums": [-500000000, 1, 2, 3, -500000000], "target": -1000000000}},
        {"in": {"nums": [1, 5, 1, 5, 9, 2], "target": 11}},
        {"in": {"nums": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], "target": 190}},
        {"in": {"nums": s1, "target": 900000000}},
        {"in": {"nums": s2, "target": -700000000}},
    ]
