import random


def visible():
    return [
        {"in": {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]}},
        {"in": {"lists": []}},
        {"in": {"lists": [[-2, -1], [], [0, 3]]}},
    ]


def hidden():
    rng1 = random.Random(23)
    stress1 = [sorted(rng1.randint(-10000, 10000) for _ in range(60)) for _ in range(50)]
    rng2 = random.Random(230)
    stress2 = [sorted(rng2.randint(-10000, 10000) for _ in range(rng2.randint(0, 25))) for _ in range(200)]
    return [
        {"in": {"lists": [[]]}},
        {"in": {"lists": [[], [], [], []]}},
        {"in": {"lists": [[42]]}},
        {"in": {"lists": [[1, 2, 3, 4, 5]]}},
        {"in": {"lists": [[], [1, 3], [], [2, 4], []]}},
        {"in": {"lists": [[5, 5], [5], [5, 5, 5], [5]]}},
        {"in": {"lists": [[-10000, 0, 10000], [-10000, -1], [1, 10000]]}},
        {"in": {"lists": [[i] for i in range(50, -50, -1)]}},
        {"in": {"lists": stress1}},
        {"in": {"lists": stress2}},
    ]
