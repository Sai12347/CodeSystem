import random


def visible():
    return [
        {"in": {"nums": [5, 2, 3, 1]}},
        {"in": {"nums": [5, 1, 1, 2, 0, 0]}},
        {"in": {"nums": [-4, 0, 7, 4, 9, -5, -1, 0, -7, -1]}},
    ]


def hidden():
    rng1 = random.Random(912)
    rng2 = random.Random(913)
    nearly_sorted = list(range(-1000, 1000))
    for _ in range(150):
        i = rng2.randrange(len(nearly_sorted))
        j = rng2.randrange(len(nearly_sorted))
        nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]

    return [
        {"in": {"nums": [42]}},
        {"in": {"nums": [2, -2]}},
        {"in": {"nums": [7] * 15}},
        {"in": {"nums": list(range(-15, 16))}},
        {"in": {"nums": list(range(25, -26, -1))}},
        {"in": {"nums": [-50000, 50000, 0, -50000, 50000, -1, 1]}},
        {"in": {"nums": [100, -100, 99, -99, 98, -98, 0, 0, 1, -1]}},
        {"in": {"nums": [3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2]}},
        {"in": {"nums": [rng1.randint(-50000, 50000) for _ in range(2500)]}},
        {"in": {"nums": nearly_sorted}},
    ]
