import random


def visible():
    return [
        {"in": {"citations": [3, 0, 6, 1, 5]}},
        {"in": {"citations": [1, 3, 1]}},
        {"in": {"citations": [0, 0, 0]}},
    ]


def hidden():
    rng1 = random.Random(274)
    rng2 = random.Random(275)
    stress1 = [rng1.randint(0, 1000) for _ in range(1500)]
    stress2 = [rng2.randint(0, 50) for _ in range(1000)] + [rng2.randint(500, 1000) for _ in range(500)]
    rng2.shuffle(stress2)

    return [
        {"in": {"citations": [0]}},
        {"in": {"citations": [1]}},
        {"in": {"citations": [100]}},
        {"in": {"citations": [10, 10, 10, 10]}},
        {"in": {"citations": [4, 4, 0, 0]}},
        {"in": {"citations": [0, 1, 2, 3, 4, 5]}},
        {"in": {"citations": [5, 4, 3, 2, 1]}},
        {"in": {"citations": [1, 1, 1, 1, 1, 1]}},
        {"in": {"citations": [1000] * 50}},
        {"in": {"citations": [0, 1, 3, 5, 6]}},
        {"in": {"citations": stress1}},
        {"in": {"citations": stress2}},
    ]
