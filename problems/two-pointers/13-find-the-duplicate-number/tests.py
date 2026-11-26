import random


def visible():
    return [
        {"in": {"nums": [1, 3, 4, 2, 2]}},
        {"in": {"nums": [3, 1, 3, 4, 2]}},
        {"in": {"nums": [3, 3, 3, 3, 3]}},
    ]


def hidden():
    rng = random.Random(287)

    # Stress test 1: n = 3000, duplicate 1729 appears twice
    arr1 = list(range(1, 3001)) + [1729]
    rng.shuffle(arr1)

    # Stress test 2: n = 4000, duplicate 2500 appears 5 times
    arr2 = [x for x in range(1, 4001) if x not in (10, 20, 30, 40)] + [2500] * 5
    rng.shuffle(arr2)

    return [
        {"in": {"nums": [1, 1]}},
        {"in": {"nums": [2, 1, 3, 4, 1]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 5]}},
        {"in": {"nums": [2, 5, 9, 6, 9, 3, 8, 9, 7, 1]}},
        {"in": {"nums": [2, 1, 3, 4, 2]}},
        {"in": {"nums": [1, 4, 4, 2, 4]}},
        {"in": {"nums": [5, 4, 3, 2, 1, 3]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 8]}},
        {"in": {"nums": arr1}},
        {"in": {"nums": arr2}},
    ]
