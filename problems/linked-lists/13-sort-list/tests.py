import random


def visible():
    return [
        {"in": {"head": [4, 2, 1, 3]}},
        {"in": {"head": [-1, 5, 3, 4, 0]}},
        {"in": {"head": []}},
    ]


def hidden():
    rng = random.Random(148)
    stress_rand = [rng.randint(-100000, 100000) for _ in range(3000)]
    stress_rev = [2000 - (i // 2) for i in range(4000)]

    return [
        # Single node
        {"in": {"head": [7]}},
        # Two elements already sorted
        {"in": {"head": [1, 2]}},
        # Two elements reversed
        {"in": {"head": [2, 1]}},
        # All equal elements
        {"in": {"head": [5, 5, 5, 5, 5, 5]}},
        # Already sorted with negatives
        {"in": {"head": [-10, -5, 0, 3, 8, 12, 100]}},
        # Strictly reverse sorted
        {"in": {"head": [100, 50, 10, 0, -10, -50, -100]}},
        # Extreme constraint boundaries and duplicates
        {"in": {"head": [-100000, 100000, 0, -100000, 100000, -1, 1]}},
        # Odd length with repeating pattern
        {"in": {"head": [3, 1, 2, 3, 1, 2, 3, 1, 2]}},
        # Stress: 3000 random values
        {"in": {"head": stress_rand}},
        # Stress: 4000 reverse-sorted with duplicates
        {"in": {"head": stress_rev}},
    ]
