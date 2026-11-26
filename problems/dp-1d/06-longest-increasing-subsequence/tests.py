import random


def visible():
    return [
        {"in": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}},
        {"in": {"nums": [0, 1, 0, 3, 2, 3]}},
        {"in": {"nums": [7, 7, 7, 7, 7, 7, 7]}},
    ]


def hidden():
    rng1 = random.Random(300)
    rng2 = random.Random(3000)
    sawtooth = [((i % 50) * 10 - (i // 50)) for i in range(1500)]
    return [
        {"in": {"nums": [42]}},
        {"in": {"nums": [-5, 10]}},
        {"in": {"nums": [10, -5]}},
        {"in": {"nums": [-10, -20, -15, -5, -1, -8, 0]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"nums": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": [4, 10, 4, 3, 8, 9]}},
        {"in": {"nums": [-10000, 10000, -9999, 0, 9999, 10000]}},
        {"in": {"nums": [rng1.randint(-1000, 1000) for _ in range(100)]}},
        {"in": {"nums": sawtooth}},
        {"in": {"nums": [rng2.randint(-10000, 10000) for _ in range(2000)]}},
    ]
