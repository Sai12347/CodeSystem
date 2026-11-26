import random


def visible():
    return [
        {"in": {"intervals": [[1, 3], [2, 6], [8, 10], [15, 18]]}},
        {"in": {"intervals": [[1, 4], [4, 5]]}},
        {"in": {"intervals": [[2, 3], [1, 4]]}},
    ]


def hidden():
    rng1 = random.Random(56)
    rng2 = random.Random(57)
    stress1 = []
    for _ in range(1000):
        a = rng1.randint(0, 9500)
        b = a + rng1.randint(0, 30)
        stress1.append([a, b])
    stress2 = []
    for _ in range(800):
        a = rng2.randint(0, 10000)
        b = min(10000, a + rng2.randint(0, 500))
        stress2.append([a, b])

    return [
        {"in": {"intervals": [[5, 5]]}},
        {"in": {"intervals": [[0, 0], [0, 0], [0, 0]]}},
        {"in": {"intervals": [[1, 2], [3, 4], [5, 6], [7, 8]]}},
        {"in": {"intervals": [[10, 12], [7, 9], [4, 6], [1, 3]]}},
        {"in": {"intervals": [[1, 10], [2, 3], [4, 5], [6, 7], [8, 9]]}},
        {"in": {"intervals": [[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]}},
        {"in": {"intervals": [[1, 4], [0, 4]]}},
        {"in": {"intervals": [[1, 4], [0, 0]]}},
        {"in": {"intervals": [[0, 10000], [500, 600], [10000, 10000]]}},
        {"in": {"intervals": stress1}},
        {"in": {"intervals": stress2}},
    ]
