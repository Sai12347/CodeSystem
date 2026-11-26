import random


def visible():
    return [
        {"in": {"intervals": [[0, 30], [5, 10], [15, 20]]}},
        {"in": {"intervals": [[7, 10], [2, 4]]}},
        {"in": {"intervals": [[1, 5], [5, 10], [10, 15]]}},
    ]


def hidden():
    rng1 = random.Random(253)
    rng2 = random.Random(254)
    stress1 = []
    for _ in range(1000):
        s = rng1.randint(0, 990000)
        e = s + rng1.randint(1, 10000)
        stress1.append([s, e])
    stress2 = []
    for _ in range(1000):
        s = rng2.randint(0, 2000)
        e = s + rng2.randint(50, 1500)
        stress2.append([s, e])

    return [
        {"in": {"intervals": [[0, 1]]}},
        {"in": {"intervals": [[2, 8]] * 7}},
        {"in": {"intervals": [[1, 10], [2, 9], [3, 8], [4, 7], [5, 6]]}},
        {"in": {"intervals": [[1, 5], [1, 5], [5, 10], [5, 10], [2, 6]]}},
        {"in": {"intervals": [[13, 15], [1, 13], [6, 9]]}},
        {"in": {"intervals": [[0, 1000000], [999999, 1000000], [0, 1]]}},
        {"in": {"intervals": [[2, 11], [6, 16], [11, 16]]}},
        {"in": {"intervals": [[1, 4], [2, 5], [3, 6], [4, 7], [5, 8], [6, 9]]}},
        {"in": {"intervals": [[10, 20], [1, 10], [20, 30], [5, 15], [15, 25]]}},
        {"in": {"intervals": stress1}},
        {"in": {"intervals": stress2}},
    ]
