import random


def visible():
    return [
        {"in": {"nums": [23, 2, 4, 6, 7], "k": 6}},
        {"in": {"nums": [23, 2, 6, 4, 7], "k": 6}},
        {"in": {"nums": [23, 2, 6, 4, 7], "k": 13}},
    ]


def hidden():
    rng = random.Random(523)
    # 1500 elements of value 1 with k = 1501 -> never reaches a multiple of 1501 (max sum 1500)
    no_hit_big = [1] * 1500
    # 1500 elements of value 1 with k = 1500 -> entire array sums to 1500 -> True
    full_hit_big = [1] * 1500
    # Random non-negative numbers with total sum < 2^31 - 1 and large prime k
    rand_big = [rng.randint(1, 500000) for _ in range(1200)]
    return [
        {"in": {"nums": [0], "k": 1}},
        {"in": {"nums": [0, 0], "k": 1000000}},
        {"in": {"nums": [1, 0], "k": 2}},
        {"in": {"nums": [5, 0, 0, 0], "k": 3}},
        {"in": {"nums": [5, 2, 4], "k": 5}},
        {"in": {"nums": [23, 2, 4, 6, 6], "k": 7}},
        {"in": {"nums": [1, 2, 12], "k": 6}},
        {"in": {"nums": [1000000000, 1000000000], "k": 2000000000}},
        {"in": {"nums": [1000000000, 1000000000], "k": 2147483647}},
        {"in": {"nums": no_hit_big, "k": 1501}},
        {"in": {"nums": full_hit_big, "k": 1500}},
        {"in": {"nums": rand_big, "k": 1000003}},
    ]
