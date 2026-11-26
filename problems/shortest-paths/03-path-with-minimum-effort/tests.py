import random


def visible():
    return [
        {"in": {"heights": [[1, 2, 2], [3, 8, 2], [5, 3, 5]]}},
        {"in": {"heights": [[1, 2, 3], [3, 8, 4], [5, 3, 5]]}},
        {"in": {"heights": [
            [1, 2, 1, 1, 1],
            [1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1],
            [1, 1, 1, 2, 1],
        ]}},
    ]


def hidden():
    tests = []

    # 1. Single cell
    tests.append({"in": {"heights": [[42]]}})

    # 2. Single row
    tests.append({"in": {"heights": [[1, 10, 6, 7, 9, 10, 4, 9]]}})

    # 3. Single column
    tests.append({"in": {"heights": [[1], [5], [2], [10], [8]]}})

    # 4. All-equal heights at upper bound
    tests.append({"in": {"heights": [[1000000] * 5 for _ in range(5)]}})

    # 5. Maximum height difference boundary
    tests.append({"in": {"heights": [[1, 1000000]]}})

    # 6. Must move UP and LEFT through a snake corridor (breaks down/right-only DP)
    tests.append({"in": {"heights": [
        [1, 100, 1, 1, 1],
        [1, 100, 1, 100, 1],
        [1, 100, 1, 100, 1],
        [1, 1, 1, 100, 1],
        [100, 100, 100, 100, 1],
    ]}})

    # 7. Decreasing ramp with cliff barrier
    tests.append({"in": {"heights": [
        [50, 45, 40, 35],
        [10, 10, 10, 30],
        [20, 25, 22, 25],
        [18, 19, 20, 20],
    ]}})

    # 8. Tight two-path tradeoff: smooth long detour vs sharp short jump
    tests.append({"in": {"heights": [
        [10, 12, 14, 16, 18],
        [50, 50, 50, 50, 20],
        [28, 26, 24, 22, 22],
        [30, 90, 90, 90, 90],
        [32, 34, 36, 38, 40],
    ]}})

    # 9. Medium random grid (30x30)
    rng = random.Random(16311)
    g9 = [[rng.randint(1, 1000000) for _ in range(30)] for _ in range(30)]
    tests.append({"in": {"heights": g9}})

    # 10. Stress test: larger random grid (55x55)
    rng2 = random.Random(16312)
    g10 = [[rng2.randint(1, 1000000) for _ in range(55)] for _ in range(55)]
    tests.append({"in": {"heights": g10}})

    return tests
