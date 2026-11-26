import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 1]}},
        {"in": {"nums": [1, 2, 1, 3, 5, 6, 4]}},
        {"in": {"nums": [1]}},
    ]


def hidden():
    rng1 = random.Random(1621)
    large1 = []
    prev = None
    for _ in range(1000):
        val = rng1.randint(-100000, 100000)
        while val == prev:
            val = rng1.randint(-100000, 100000)
        large1.append(val)
        prev = val

    large2 = list(range(-500, 500))

    return [
        {"in": {"nums": [1, 2, 3, 4, 5, 6]}},
        {"in": {"nums": [6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": [1, 2]}},
        {"in": {"nums": [2, 1]}},
        {"in": {"nums": [-2147483648]}},
        {"in": {"nums": [-2147483648, 2147483647, -2147483648]}},
        {"in": {"nums": [1, 3, 2, 4, 3, 5, 4, 6, 5]}},
        {"in": {"nums": [10, 5, 2, 1, 3, 7, 12]}},
        {"in": {"nums": [-100, -50, -80, -20, -30]}},
        {"in": {"nums": large1}},
        {"in": {"nums": large2}},
    ]
