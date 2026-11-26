import random


def visible():
    return [
        {"in": {"pages": [12, 34, 67, 90], "students": 2}},
        {"in": {"pages": [15, 17, 20], "students": 5}},
        {"in": {"pages": [22, 23, 67], "students": 1}},
    ]


def hidden():
    rng1 = random.Random(1401)
    stress1 = [rng1.randint(1, 10000) for _ in range(2000)]

    rng2 = random.Random(1402)
    stress2 = [rng2.randint(1, 10000) for _ in range(4000)]

    return [
        {"in": {"pages": [50], "students": 1}},
        {"in": {"pages": [50], "students": 2}},
        {"in": {"pages": [10, 20, 30, 40], "students": 4}},
        {"in": {"pages": [10, 20, 30, 40], "students": 5}},
        {"in": {"pages": [25, 25, 25, 25, 25], "students": 3}},
        {"in": {"pages": [10, 20, 30, 40], "students": 2}},
        {"in": {"pages": [1, 1, 1, 10000, 1, 1], "students": 3}},
        {"in": {"pages": [90, 67, 34, 12], "students": 2}},
        {"in": {"pages": stress1, "students": 50}},
        {"in": {"pages": stress2, "students": 400}},
    ]
