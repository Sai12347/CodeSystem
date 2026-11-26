import random


def visible():
    return [
        {"in": {"head": [1, 2, 3, 4, 5], "k": 2}},
        {"in": {"head": [1, 2, 3, 4, 5], "k": 3}},
    ]


def hidden():
    rng = random.Random(25)
    large1 = [rng.randint(0, 1000) for _ in range(3000)]
    large2 = [rng.randint(0, 1000) for _ in range(3000)]

    return [
        # Single node, k = 1
        {"in": {"head": [42], "k": 1}},
        # k = 1 on multi-node list (no change)
        {"in": {"head": [10, 20, 30, 40, 50], "k": 1}},
        # k = n (reverse entire list)
        {"in": {"head": [1, 2, 3, 4, 5], "k": 5}},
        # Exact multiple of k = 2
        {"in": {"head": [1, 2, 3, 4, 5, 6], "k": 2}},
        # Exact multiple of k = 3
        {"in": {"head": [1, 2, 3, 4, 5, 6], "k": 3}},
        # k = n - 1 (single leftover node)
        {"in": {"head": [1, 2, 3, 4, 5, 6], "k": 5}},
        # Duplicates and zeros
        {"in": {"head": [0, 0, 1, 1, 0, 0, 2], "k": 3}},
        # Minimum pair reversal
        {"in": {"head": [999, 1000], "k": 2}},
        # Stress: n = 3000, k = 7 (remainder 4)
        {"in": {"head": large1, "k": 7}},
        # Stress: n = 3000, k = 3000 (entire list reversed iteratively)
        {"in": {"head": large2, "k": 3000}},
    ]
