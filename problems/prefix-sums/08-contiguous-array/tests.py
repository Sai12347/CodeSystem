import random


def visible():
    return [
        {"in": {"nums": [0, 1]}},
        {"in": {"nums": [0, 1, 0]}},
        {"in": {"nums": [0, 1, 1, 1, 1, 1, 0, 0, 0]}},
    ]


def hidden():
    rng1 = random.Random(5251)
    stress1 = [rng1.randint(0, 1) for _ in range(2000)]

    rng2 = random.Random(5252)
    stress2 = [0] * 400 + [rng2.randint(0, 1) for _ in range(2200)] + [1] * 400

    return [
        {"in": {"nums": [0]}},
        {"in": {"nums": [1]}},
        {"in": {"nums": [0, 0, 0, 0, 0]}},
        {"in": {"nums": [1, 1, 1, 1, 1, 1]}},
        {"in": {"nums": [1, 0, 1, 0, 1, 0, 1]}},
        {"in": {"nums": [1, 1, 1, 0, 0, 1, 0, 1, 1, 1]}},
        {"in": {"nums": [0] * 10 + [1] * 10}},
        {"in": {"nums": [0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0]}},
        {"in": {"nums": [0, 0, 1, 0, 0, 0, 1, 1]}},
        {"in": {"nums": stress1}},
        {"in": {"nums": stress2}},
    ]
