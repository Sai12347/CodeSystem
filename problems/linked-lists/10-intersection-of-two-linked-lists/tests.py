import random


def visible():
    return [
        {"in": {"listA": [4, 1, 8, 4, 5], "listB": [5, 6, 1, 8, 4, 5], "skipA": 2, "skipB": 3}},
        {"in": {"listA": [1, 9, 1, 2, 4], "listB": [3, 2, 4], "skipA": 3, "skipB": 1}},
        {"in": {"listA": [2, 6, 4], "listB": [1, 5], "skipA": 3, "skipB": 2}},
    ]


def hidden():
    rng1 = random.Random(160)
    shared1 = [rng1.randint(1, 100000) for _ in range(500)]
    prefA1 = [rng1.randint(1, 100000) for _ in range(1000)]
    prefB1 = [rng1.randint(1, 100000) for _ in range(700)]

    rng2 = random.Random(161)
    disjA = [rng2.randint(1, 100000) for _ in range(1000)]
    disjB = [rng2.randint(1, 100000) for _ in range(1200)]

    return [
        # Single shared node
        {"in": {"listA": [1], "listB": [1], "skipA": 0, "skipB": 0}},
        # Single disjoint nodes with identical value
        {"in": {"listA": [1], "listB": [1], "skipA": 1, "skipB": 1}},
        # Identical lists intersecting at head
        {"in": {"listA": [7, 7, 7], "listB": [7, 7, 7], "skipA": 0, "skipB": 0}},
        # listB is a suffix of listA
        {"in": {"listA": [10, 20, 30, 40, 50, 60], "listB": [50, 60], "skipA": 4, "skipB": 0}},
        # listA is a suffix of listB
        {"in": {"listA": [99, 100], "listB": [1, 2, 3, 4, 5, 99, 100], "skipA": 0, "skipB": 5}},
        # Intersection at the very last node only
        {"in": {"listA": [1, 2, 3, 4, 5], "listB": [9, 8, 5], "skipA": 4, "skipB": 2}},
        # All duplicate values, intersecting in the middle (tests reference identity)
        {"in": {"listA": [5, 5, 5, 5, 5, 5], "listB": [5, 5, 5, 5], "skipA": 3, "skipB": 1}},
        # All duplicate values, no intersection
        {"in": {"listA": [5, 5, 5, 5, 5], "listB": [5, 5, 5], "skipA": 5, "skipB": 3}},
        # Large stress test with intersection
        {"in": {"listA": prefA1 + shared1, "listB": prefB1 + shared1, "skipA": len(prefA1), "skipB": len(prefB1)}},
        # Large stress test with no intersection
        {"in": {"listA": disjA, "listB": disjB, "skipA": len(disjA), "skipB": len(disjB)}},
    ]
