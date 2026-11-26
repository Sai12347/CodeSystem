import random


def visible():
    return [
        {"in": {"nums": [10, 2]}},
        {"in": {"nums": [3, 30, 34, 5, 9]}},
        {"in": {"nums": [0, 0]}},
    ]


def hidden():
    rng1 = random.Random(179)
    rng2 = random.Random(180)
    prefix_pool = [3, 30, 34, 343, 3432, 34323, 33, 330, 334, 303]
    stress_prefix = [rng1.choice(prefix_pool) for _ in range(100)]
    stress_full = [rng2.randint(0, 10**9) for _ in range(100)]

    return [
        {"in": {"nums": [0]}},
        {"in": {"nums": [1]}},
        {"in": {"nums": [0, 0, 0, 0, 0]}},
        {"in": {"nums": [0, 10, 0]}},
        {"in": {"nums": [34323, 3432]}},
        {"in": {"nums": [121, 12]}},
        {"in": {"nums": [8308, 8308, 830]}},
        {"in": {"nums": [999999991, 9]}},
        {"in": {"nums": [1000000000, 999999999, 999999998, 99, 9]}},
        {"in": {"nums": [111311, 1113]}},
        {"in": {"nums": stress_prefix}},
        {"in": {"nums": stress_full}},
    ]
