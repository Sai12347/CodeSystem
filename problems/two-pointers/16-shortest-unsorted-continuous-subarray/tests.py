import random


def visible():
    return [
        {"in": {"nums": [2, 6, 4, 8, 10, 9, 15]}},
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [1]}},
    ]


def hidden():
    rng = random.Random(581)

    # Stress test 1: sorted prefix + shuffled middle + sorted suffix
    prefix = sorted(rng.randint(-100000, -20000) for _ in range(800))
    middle = [rng.randint(-15000, 15000) for _ in range(1400)]
    suffix = sorted(rng.randint(20000, 100000) for _ in range(800))
    mid_unsorted = prefix + middle + suffix

    # Stress test 2: sorted array with two elements swapped near opposite ends
    swapped = list(range(-2000, 2000))
    swapped[10], swapped[3985] = swapped[3985], swapped[10]

    return [
        {"in": {"nums": [1, 2]}},
        {"in": {"nums": [2, 1]}},
        {"in": {"nums": [5, 5, 5, 5, 5]}},
        {"in": {"nums": [5, 4, 3, 2, 1]}},
        {"in": {"nums": [1, 3, 2, 2, 2]}},
        {"in": {"nums": [1, 2, 3, 3, 3, 2, 4, 5]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 0]}},
        {"in": {"nums": [100, 1, 2, 3, 4, 5]}},
        {"in": {"nums": [-100000, -50000, 100000, 0, 50000, 100000]}},
        {"in": {"nums": mid_unsorted}},
        {"in": {"nums": swapped}},
    ]
