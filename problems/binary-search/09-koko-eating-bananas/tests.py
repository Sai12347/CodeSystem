import random


def visible():
    return [
        {"in": {"piles": [3, 6, 7, 11], "h": 8}},
        {"in": {"piles": [30, 11, 23, 4, 20], "h": 5}},
        {"in": {"piles": [30, 11, 23, 4, 20], "h": 6}},
    ]


def hidden():
    rng1 = random.Random(875)
    stress1 = [rng1.randint(1, 1000000) for _ in range(2000)]

    rng2 = random.Random(87502)
    stress2 = [rng2.randint(1, 1000000000) for _ in range(3000)]

    return [
        {"in": {"piles": [100], "h": 1}},
        {"in": {"piles": [5], "h": 10}},
        {"in": {"piles": [10], "h": 3}},
        {"in": {"piles": [7, 7, 7, 7], "h": 4}},
        {"in": {"piles": [1, 1, 1, 1, 1], "h": 1000000000}},
        {"in": {"piles": [805306368, 805306368, 805306368], "h": 1000000000}},
        {"in": {"piles": [1000000000, 1000000000, 1000000000, 1000000000], "h": 1000000000}},
        {"in": {"piles": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10], "h": 15}},
        {"in": {"piles": stress1, "h": 5000}},
        {"in": {"piles": stress2, "h": 50000}},
    ]
