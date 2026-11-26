import random


def visible():
    return [
        {"in": {"deck": [17, 13, 11, 2, 3, 5, 7]}},
        {"in": {"deck": [1, 1000]}},
    ]


def hidden():
    rng1 = random.Random(950)
    big1 = rng1.sample(range(1, 1_000_001), 500)

    rng2 = random.Random(9500)
    big2 = rng2.sample(range(1, 1_000_001), 1000)

    return [
        {"in": {"deck": [42]}},
        {"in": {"deck": [100, 1]}},
        {"in": {"deck": [3, 1, 2]}},
        {"in": {"deck": list(range(1, 11))}},
        {"in": {"deck": list(range(10, 0, -1))}},
        {"in": {"deck": [16, 4, 8, 2, 12, 6, 14, 1, 15, 3, 9, 5, 11, 7, 13, 10]}},
        {"in": {"deck": list(range(1, 16))}},
        {"in": {"deck": [1, 1000000, 500000, 999999, 2]}},
        {"in": {"deck": big1}},
        {"in": {"deck": big2}},
    ]
