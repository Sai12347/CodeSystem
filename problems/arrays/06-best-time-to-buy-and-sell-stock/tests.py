import random


def visible():
    return [
        {"in": {"prices": [7, 1, 5, 3, 6, 4]}},
        {"in": {"prices": [7, 6, 4, 3, 1]}},
        {"in": {"prices": [2, 4, 1]}},
    ]


def hidden():
    rng = random.Random(606)
    s1 = [rng.randint(0, 10000) for _ in range(2000)]
    s2 = list(range(3000, 1000, -1)) + [500, 9500] + list(range(9499, 9000, -1))
    return [
        {"in": {"prices": [5]}},
        {"in": {"prices": [0, 0, 0, 0]}},
        {"in": {"prices": [1, 2]}},
        {"in": {"prices": [2, 1]}},
        {"in": {"prices": [0, 10000]}},
        {"in": {"prices": [3, 2, 6, 5, 0, 3]}},
        {"in": {"prices": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"prices": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"prices": [5, 5, 5, 1, 5, 5, 5]}},
        {"in": {"prices": s1}},
        {"in": {"prices": s2}},
    ]
