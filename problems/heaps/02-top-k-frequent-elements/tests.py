import random


def visible():
    return [
        {"in": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}},
        {"in": {"nums": [1], "k": 1}},
        {"in": {"nums": [-1, -1, -1, 4, 4, 2, 0], "k": 2}},
    ]


def hidden():
    # Stress 1: 40 distinct elements with strictly decreasing frequencies 50..11, shuffled
    rng1 = random.Random(34701)
    stress1 = []
    for idx in range(40):
        val = (idx - 20) * 17
        stress1.extend([val] * (50 - idx))
    rng1.shuffle(stress1)

    # Stress 2: top 15 elements have frequencies 30..44, noise has frequencies 1..10
    rng2 = random.Random(34702)
    stress2 = []
    for i in range(15):
        stress2.extend([1000 + i] * (30 + i))
    for j in range(120):
        stress2.extend([-5000 + j] * rng2.randint(1, 10))
    rng2.shuffle(stress2)

    return [
        {"in": {"nums": [5, 5, 5, 5], "k": 1}},
        {"in": {"nums": [1, 2, 3, 4], "k": 4}},
        {"in": {"nums": [-10000, -10000, 10000, 10000, 10000, 0], "k": 1}},
        {"in": {"nums": [-10000, -10000, 10000, 10000, 10000, 0], "k": 2}},
        {"in": {"nums": [0, 0, 1, 1, 1, 2, 2, 2, 2, 3], "k": 3}},
        {"in": {"nums": [9, 8, 7, 9, 8, 9, 6, 5, 4, 8, 8], "k": 2}},
        {"in": {"nums": [-5, -5, -5, -4, -4, -3, -3, -2, -1], "k": 1}},
        {"in": {"nums": [4, 1, -1, 2, -1, 2, 3], "k": 2}},
        {"in": {"nums": stress1, "k": 10}},
        {"in": {"nums": stress2, "k": 15}},
    ]
