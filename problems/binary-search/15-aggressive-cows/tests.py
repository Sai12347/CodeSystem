import random


def visible():
    return [
        {"in": {"stalls": [1, 2, 8, 4, 9], "cows": 3}},
        {"in": {"stalls": [1, 2, 3, 4, 7], "cows": 3}},
        {"in": {"stalls": [5, 4, 3, 2, 1, 1000000000], "cows": 2}},
    ]


def hidden():
    rng1 = random.Random(1552)
    stress1 = rng1.sample(range(0, 1000001), 2000)

    rng2 = random.Random(155202)
    stress2 = rng2.sample(range(0, 1000000001), 3000)

    return [
        {"in": {"stalls": [0, 1], "cows": 2}},
        {"in": {"stalls": [1000000000, 0], "cows": 2}},
        {"in": {"stalls": [10, 3, 7, 15, 22], "cows": 5}},
        {"in": {"stalls": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "cows": 4}},
        {"in": {"stalls": [100, 80, 60, 40, 20, 0], "cows": 3}},
        {"in": {"stalls": [1, 2, 3, 100, 101, 102], "cows": 3}},
        {"in": {"stalls": [1, 2, 3, 100, 101, 102], "cows": 4}},
        {"in": {"stalls": [0, 100000000, 200000000, 500000000, 700000000, 1000000000], "cows": 4}},
        {"in": {"stalls": stress1, "cows": 50}},
        {"in": {"stalls": stress2, "cows": 200}},
    ]
