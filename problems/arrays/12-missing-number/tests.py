import random


def visible():
    return [
        {"in": {"nums": [3, 0, 1]}},
        {"in": {"nums": [0, 1]}},
        {"in": {"nums": [9, 6, 4, 2, 3, 5, 7, 0, 1]}},
    ]


def hidden():
    rng = random.Random(268)
    s1 = list(range(3001))
    s1.remove(1729)
    rng.shuffle(s1)

    s2 = list(range(5000))
    rng.shuffle(s2)

    return [
        {"in": {"nums": [0]}},
        {"in": {"nums": [1]}},
        {"in": {"nums": [1, 2]}},
        {"in": {"nums": [0, 1, 2, 3, 4]}},
        {"in": {"nums": [4, 3, 2, 1]}},
        {"in": {"nums": [5, 4, 3, 2, 0]}},
        {"in": {"nums": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"nums": [10, 9, 8, 7, 6, 4, 3, 2, 1, 0]}},
        {"in": {"nums": s1}},
        {"in": {"nums": s2}},
    ]
