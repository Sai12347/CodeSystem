import random


def visible():
    h1 = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4],
    ]
    h2 = [[1]]
    h3 = [
        [5, 5],
        [5, 5],
    ]
    return [
        {"in": {"heights": h1}},
        {"in": {"heights": h2}},
        {"in": {"heights": h3}},
    ]


def hidden():
    tests = []

    # 1. Single cell with height 0
    tests.append({"in": {"heights": [[0]]}})

    # 2. Single row (every cell touches both top=Pacific and bottom=Atlantic)
    tests.append({"in": {"heights": [[10, 3, 7, 1, 9, 2]]}})

    # 3. Single column (every cell touches both left=Pacific and right=Atlantic)
    tests.append({"in": {"heights": [[8], [2], [6], [6], [1], [9]]}})

    # 4. Strictly increasing toward bottom-right
    inc = [[r * 5 + c for c in range(5)] for r in range(5)]
    tests.append({"in": {"heights": inc}})

    # 5. Strictly decreasing toward bottom-right
    dec = [[(4 - r) * 5 + (4 - c) for c in range(5)] for r in range(5)]
    tests.append({"in": {"heights": dec}})

    # 6. Central valley surrounded by high walls
    valley = [
        [9, 9, 9, 9, 9],
        [9, 2, 2, 2, 9],
        [9, 2, 0, 2, 9],
        [9, 2, 2, 2, 9],
        [9, 9, 9, 9, 9],
    ]
    tests.append({"in": {"heights": valley}})

    # 7. Central peak sloping down to all edges
    peak = [
        [1, 2, 3, 2, 1],
        [2, 5, 7, 5, 2],
        [3, 7, 10, 7, 3],
        [2, 5, 7, 5, 2],
        [1, 2, 3, 2, 1],
    ]
    tests.append({"in": {"heights": peak}})

    # 8. All equal max-constraint heights (10^5)
    tests.append({"in": {"heights": [[100000] * 6 for _ in range(6)]}})

    # 9. Winding ridge requiring sideways flow around lower obstacles
    ridge = [
        [1, 1, 1, 1, 1, 1, 1, 8],
        [1, 9, 9, 9, 9, 9, 1, 8],
        [1, 9, 2, 2, 2, 9, 1, 8],
        [1, 9, 2, 10, 2, 9, 1, 8],
        [1, 9, 2, 10, 10, 9, 1, 8],
        [1, 9, 2, 2, 10, 1, 1, 8],
        [1, 9, 9, 9, 10, 10, 10, 8],
        [8, 8, 8, 8, 8, 8, 8, 8],
    ]
    tests.append({"in": {"heights": ridge}})

    # 10. Medium random grid (30x30) with wide height range
    rng1 = random.Random(4171)
    g10 = [[rng1.randint(0, 100000) for _ in range(30)] for _ in range(30)]
    tests.append({"in": {"heights": g10}})

    # 11. Larger terrain grid (45x45) with moderate plateaus to test long equal-height paths
    rng2 = random.Random(4172)
    g11 = [[rng2.randint(0, 25) for _ in range(45)] for _ in range(45)]
    tests.append({"in": {"heights": g11}})

    return tests
