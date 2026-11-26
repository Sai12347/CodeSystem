import random


def visible():
    return [
        {"in": {"fruits": [1, 2, 1]}},
        {"in": {"fruits": [0, 1, 2, 2]}},
        {"in": {"fruits": [1, 2, 3, 2, 2]}},
    ]


def hidden():
    rng1 = random.Random(904)
    stress1 = [rng1.randint(0, 7) for _ in range(3500)]

    rng2 = random.Random(905)
    stress2 = []
    for block in range(70):
        a, b = rng2.randint(0, 3499), rng2.randint(0, 3499)
        for _ in range(49):
            stress2.append(a if rng2.random() < 0.5 else b)
        stress2.append(rng2.randint(0, 3499))

    return [
        {"in": {"fruits": [0]}},
        {"in": {"fruits": [0, 0]}},
        {"in": {"fruits": [0, 1]}},
        {"in": {"fruits": [0] * 10}},
        {"in": {"fruits": [0, 1, 2, 3, 4, 5, 6, 7]}},
        {"in": {"fruits": [3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]}},
        {"in": {"fruits": [0, 1, 0, 1, 2, 3, 2, 3, 2, 3, 2]}},
        {"in": {"fruits": [2, 1, 2, 1, 2, 1, 0, 3, 4, 5, 6]}},
        {"in": {"fruits": [5, 4, 5, 4, 3, 5]}},
        {"in": {"fruits": stress1}},
        {"in": {"fruits": stress2}},
    ]
