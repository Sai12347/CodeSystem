import random


def visible():
    return [
        {"in": {"nums": [-1, 2, 1, -4], "target": 1}},
        {"in": {"nums": [0, 0, 0], "target": 1}},
        {"in": {"nums": [4, 0, 5, -5, 3, 3, 0, -4, -5], "target": -2}},
    ]


def hidden():
    rng1 = random.Random(201)
    arr1 = [rng1.randint(-1000, 1000) for _ in range(120)]

    rng2 = random.Random(202)
    arr2 = [rng2.randint(-1000, 1000) for _ in range(300)]

    return [
        {"in": {"nums": [-1000, -1000, -1000], "target": -10000}},
        {"in": {"nums": [1000, 1000, 1000], "target": 10000}},
        {"in": {"nums": [5, 5, 5, 5, 5, 5], "target": 10}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7], "target": 100}},
        {"in": {"nums": [10, 8, 6, 4, 2, 0, -2], "target": -50}},
        {"in": {"nums": [-3, -2, -5, 3, -4], "target": -1}},
        {"in": {"nums": [1, 2, 4, 8, 16, 32, 64, 128], "target": 82}},
        {"in": {"nums": [-10, -3, 1, 7, 15, 22], "target": 17}},
        {"in": {"nums": arr1, "target": 347}},
        {"in": {"nums": arr2, "target": -1234}},
    ]
