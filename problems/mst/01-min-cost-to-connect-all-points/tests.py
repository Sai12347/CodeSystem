import random


def visible():
    return [
        {"in": {"points": [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]}},
        {"in": {"points": [[3, 12], [-2, 5], [-4, 1]]}},
        {"in": {"points": [[0, 0], [1, 1], [1, 0], [-1, 1]]}},
    ]


def _gen_unique_points(rng, n, lo, hi):
    seen = set()
    pts = []
    while len(pts) < n:
        p = (rng.randint(lo, hi), rng.randint(lo, hi))
        if p not in seen:
            seen.add(p)
            pts.append([p[0], p[1]])
    return pts


def hidden():
    tests = []

    # 1. Single point boundary
    tests.append({"in": {"points": [[0, 0]]}})

    # 2. Extreme coordinate boundaries (2 points)
    tests.append({"in": {"points": [[-1000000, -1000000], [1000000, 1000000]]}})

    # 3. Collinear horizontal points (unsorted)
    tests.append({"in": {"points": [[-10, 5], [15, 5], [0, 5], [-2, 5], [3, 5]]}})

    # 4. Collinear vertical points (reverse sorted)
    tests.append({"in": {"points": [[7, 100], [7, 25], [7, 0], [7, -50], [7, -100]]}})

    # 5. All negative coordinates
    tests.append({"in": {"points": [[-5, -5], [-1, -2], [-8, -1], [-3, -9], [-2, -2], [-10, -10]]}})

    # 6. Symmetric square with center (multiple equal-cost MSTs)
    tests.append({"in": {"points": [[0, 0], [0, 10], [10, 0], [10, 10], [5, 5], [0, 5], [10, 5], [5, 0], [5, 10]]}})

    # 7. Two distant clusters (only one long bridge should be taken)
    cluster_a = [[-500000 + i, -500000 + (i % 3)] for i in range(6)]
    cluster_b = [[500000 + i, 500000 - (i % 3)] for i in range(6)]
    tests.append({"in": {"points": cluster_a + cluster_b}})

    # 8. Diagonal staircase
    tests.append({"in": {"points": [[i * 3, i * 3] for i in range(15, -1, -1)]}})

    # 9. Medium random
    rng1 = random.Random(1584)
    tests.append({"in": {"points": _gen_unique_points(rng1, 80, -10000, 10000)}})

    # 10. Larger stress test
    rng2 = random.Random(158402)
    tests.append({"in": {"points": _gen_unique_points(rng2, 350, -1000000, 1000000)}})

    return tests
