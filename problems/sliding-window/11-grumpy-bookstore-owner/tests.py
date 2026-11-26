import random


def visible():
    return [
        {"in": {"customers": [1, 0, 1, 2, 1, 1, 7, 5], "grumpy": [0, 1, 0, 1, 0, 1, 0, 1], "minutes": 3}},
        {"in": {"customers": [1], "grumpy": [0], "minutes": 1}},
        {"in": {"customers": [4, 10, 10], "grumpy": [1, 1, 0], "minutes": 2}},
    ]


def hidden():
    rng1 = random.Random(1052)
    c1 = [rng1.randint(0, 1000) for _ in range(1500)]
    g1 = [rng1.randint(0, 1) for _ in range(1500)]

    rng2 = random.Random(10520)
    c2 = [rng2.randint(0, 1000) for _ in range(2000)]
    g2 = [1 if rng2.random() < 0.35 else 0 for _ in range(2000)]

    return [
        {"in": {"customers": [5], "grumpy": [1], "minutes": 1}},
        {"in": {"customers": [3, 5, 2, 8, 4], "grumpy": [0, 0, 0, 0, 0], "minutes": 2}},
        {"in": {"customers": [10, 20, 30, 40], "grumpy": [1, 1, 1, 1], "minutes": 4}},
        {"in": {"customers": [3, 9, 2, 7, 1], "grumpy": [1, 1, 1, 1, 1], "minutes": 1}},
        {"in": {"customers": [0, 0, 0, 0], "grumpy": [1, 0, 1, 0], "minutes": 2}},
        {"in": {"customers": [100, 100, 1, 1, 50, 50], "grumpy": [1, 1, 0, 0, 0, 0], "minutes": 2}},
        {"in": {"customers": [500, 500, 200, 200, 500, 500], "grumpy": [0, 0, 1, 1, 0, 0], "minutes": 2}},
        {"in": {"customers": [1000, 1000, 1000, 1000, 1000], "grumpy": [1, 0, 1, 1, 0], "minutes": 2}},
        {"in": {"customers": c1, "grumpy": g1, "minutes": 250}},
        {"in": {"customers": c2, "grumpy": g2, "minutes": 17}},
    ]
