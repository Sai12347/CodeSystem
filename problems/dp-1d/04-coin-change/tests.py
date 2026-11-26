import random


def visible():
    return [
        {"in": {"coins": [1, 2, 5], "amount": 11}},
        {"in": {"coins": [2], "amount": 3}},
        {"in": {"coins": [1], "amount": 0}},
    ]


def hidden():
    rng = random.Random(322)
    stress_coins = sorted(rng.sample(range(5, 600), 12))
    return [
        {"in": {"coins": [5, 10], "amount": 0}},
        {"in": {"coins": [7], "amount": 49}},
        {"in": {"coins": [5, 10, 25], "amount": 3}},
        {"in": {"coins": [1, 3, 4], "amount": 6}},
        {"in": {"coins": [2147483647, 1, 2], "amount": 5}},
        {"in": {"coins": [2, 5, 10, 1], "amount": 27}},
        {"in": {"coins": [1, 5, 10, 25, 100], "amount": 100}},
        {"in": {"coins": [186, 419, 83, 408], "amount": 6249}},
        {"in": {"coins": [3, 7, 405, 436], "amount": 8839}},
        {"in": {"coins": [2, 4, 6, 8, 10], "amount": 9999}},
        {"in": {"coins": stress_coins, "amount": 10000}},
    ]
