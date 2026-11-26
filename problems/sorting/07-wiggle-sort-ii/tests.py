import random


def visible():
    return [
        {"in": {"nums": [1, 5, 1, 1, 6, 4]}},
        {"in": {"nums": [1, 3, 2, 2, 3, 1]}},
        {"in": {"nums": [4, 5, 5, 6]}},
    ]


def hidden():
    rng1 = random.Random(324)
    rng2 = random.Random(325)

    # Guarantee valid wiggle inputs by constructing distinct-enough or bounded-frequency multisets
    # Stress 1: 2000 elements with values 0..5000 (very low collision rate -> guaranteed valid)
    stress1 = [rng1.randint(0, 5000) for _ in range(2000)]
    # Stress 2: 1999 elements (odd length) with heavy median duplicates (999 copies of 2500, 500 smaller, 500 larger)
    stress2 = [2500] * 999 + [rng2.randint(0, 2499) for _ in range(500)] + [rng2.randint(2501, 5000) for _ in range(500)]
    rng2.shuffle(stress2)

    return [
        {"in": {"nums": [7]}},
        {"in": {"nums": [2, 1]}},
        {"in": {"nums": [1, 1, 2]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6]}},
        {"in": {"nums": [6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": [1, 1, 2, 1, 2, 2, 1]}},
        {"in": {"nums": [0, 5000, 0, 5000, 0, 5000]}},
        {"in": {"nums": [5, 3, 1, 2, 6, 7, 8, 5, 5]}},
        {"in": {"nums": [3, 2, 1, 1, 3, 2]}},
        {"in": {"nums": stress1}},
        {"in": {"nums": stress2}},
    ]
