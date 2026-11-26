import random


def visible():
    return [
        {"in": {"cardPoints": [1, 2, 3, 4, 5, 6, 1], "k": 3}},
        {"in": {"cardPoints": [2, 2, 2], "k": 2}},
        {"in": {"cardPoints": [9, 7, 7, 9, 7, 7, 9], "k": 7}},
    ]


def hidden():
    rng1 = random.Random(1423)
    big1 = [rng1.randint(1, 10000) for _ in range(2000)]

    rng2 = random.Random(14230)
    big2 = [rng2.randint(1, 10000) for _ in range(2000)]

    return [
        {"in": {"cardPoints": [100], "k": 1}},
        {"in": {"cardPoints": [5, 1000, 10], "k": 1}},
        {"in": {"cardPoints": [10, 9, 8, 1, 1, 1, 2], "k": 3}},
        {"in": {"cardPoints": [2, 1, 1, 1, 8, 9, 10], "k": 3}},
        {"in": {"cardPoints": [1, 100, 1, 1, 1, 2, 2], "k": 2}},
        {"in": {"cardPoints": [100, 40, 17, 9, 73, 75], "k": 3}},
        {"in": {"cardPoints": [10000] * 10, "k": 10}},
        {"in": {"cardPoints": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "k": 4}},
        {"in": {"cardPoints": big1, "k": 750}},
        {"in": {"cardPoints": big2, "k": 1999}},
    ]
