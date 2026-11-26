import random


def visible():
    return [
        {"in": {"head": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]}},
        {"in": {"head": [[1, 1], [2, 1]]}},
        {"in": {"head": [[3, None], [3, 0], [3, None]]}},
    ]


def hidden():
    rng1 = random.Random(138)
    n1 = 500
    stress1 = [
        [rng1.randint(-10000, 10000), None if rng1.random() < 0.2 else rng1.randrange(n1)]
        for _ in range(n1)
    ]

    rng2 = random.Random(139)
    n2 = 1000
    stress2 = [
        [0, None if rng2.random() < 0.15 else rng2.randrange(n2)]
        for _ in range(n2)
    ]

    return [
        # Empty list
        {"in": {"head": []}},
        # Single node with null random
        {"in": {"head": [[42, None]]}},
        # Single node with self-pointing random
        {"in": {"head": [[-5, 0]]}},
        # All random pointers null
        {"in": {"head": [[1, None], [2, None], [3, None], [4, None]]}},
        # Every node's random points to itself
        {"in": {"head": [[10, 0], [20, 1], [30, 2], [40, 3]]}},
        # All random pointers point to head with identical values
        {"in": {"head": [[9, 0], [9, 0], [9, 0], [9, 0], [9, 0]]}},
        # Reverse random mapping (i -> n - 1 - i)
        {"in": {"head": [[i - 3, 6 - i] for i in range(7)]}},
        # Extreme values and duplicates with distinct random targets
        {"in": {"head": [[-10000, 3], [10000, 0], [-10000, 1], [10000, None], [0, 4]]}},
        # Stress: n = 500 with random values and random pointers
        {"in": {"head": stress1}},
        # Stress: n = 1000 all-zero values with random pointers
        {"in": {"head": stress2}},
    ]
