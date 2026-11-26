import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [-1, 1, 0, -3, 3]}},
    ]


def hidden():
    rng1 = random.Random(2381)
    stress1 = [rng1.choice([-1, 1]) for _ in range(2000)]
    for idx in rng1.sample(range(2000), 12):
        stress1[idx] = rng1.choice([-5, -4, -3, -2, 2, 3, 4, 5])

    rng2 = random.Random(2382)
    stress2 = [rng2.choice([-1, 1]) for _ in range(2500)]
    for idx in rng2.sample(range(1200), 8):
        stress2[idx] = rng2.choice([-3, -2, 2, 3])
    for idx in rng2.sample(range(1300, 2500), 8):
        stress2[idx] = rng2.choice([-3, -2, 2, 3])
    stress2[1250] = 0

    return [
        {"in": {"nums": [5, 7]}},
        {"in": {"nums": [0, -10]}},
        {"in": {"nums": [2, 0, 4, 0, 5]}},
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [1, 1, 1, 1, 1]}},
        {"in": {"nums": [-1, -1, -1, -1, -1]}},
        {"in": {"nums": [-2, -3, -4, -5]}},
        {"in": {"nums": [30, -30, 30, -30, 30, 29]}},
        {"in": {"nums": [-2, 3, -4, 5, -6, 7]}},
        {"in": {"nums": stress1}},
        {"in": {"nums": stress2}},
    ]
