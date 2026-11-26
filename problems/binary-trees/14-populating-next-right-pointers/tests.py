import random


def visible():
    return [
        {"in": {"root": [1, 2, 3, 4, 5, 6, 7]}},
        {"in": {"root": []}},
        {"in": {"root": [0]}},
    ]


def hidden():
    rng1 = random.Random(1161)
    rng2 = random.Random(1162)
    rng3 = random.Random(1163)
    return [
        # Height 2 (3 nodes) with negative values
        {"in": {"root": [-1, -2, -3]}},
        # Height 3 (7 nodes) all equal values
        {"in": {"root": [5, 5, 5, 5, 5, 5, 5]}},
        # Height 4 (15 nodes) increasing values
        {"in": {"root": list(range(1, 16))}},
        # Height 4 (15 nodes) extreme boundary values
        {"in": {"root": [1000 if i % 2 == 0 else -1000 for i in range(15)]}},
        # Height 5 (31 nodes) alternating signs
        {"in": {"root": [((-1) ** i) * (i + 1) for i in range(31)]}},
        # Height 6 (63 nodes) deterministic random
        {"in": {"root": [rng1.randint(-1000, 1000) for _ in range(63)]}},
        # Height 7 (127 nodes) reverse sorted
        {"in": {"root": list(range(127, 0, -1))}},
        # Stress 1: Height 10 (1023 nodes)
        {"in": {"root": [rng2.randint(-1000, 1000) for _ in range(1023)]}},
        # Stress 2: Height 11 (2047 nodes)
        {"in": {"root": [rng3.randint(-1000, 1000) for _ in range(2047)]}},
    ]
