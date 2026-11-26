import random


def visible():
    return [
        {"in": {"n": 3, "wells": [1, 2, 2], "pipes": [[1, 2, 1], [2, 3, 1]]}},
        {"in": {"n": 2, "wells": [1, 1], "pipes": [[1, 2, 1], [1, 2, 2]]}},
        {"in": {"n": 3, "wells": [5, 5, 5], "pipes": [[1, 2, 10], [2, 3, 10]]}},
    ]


def hidden():
    tests = []

    # 1. Single house, no pipes
    tests.append({"in": {"n": 1, "wells": [42], "pipes": []}})

    # 2. Multiple houses, no pipes at all
    tests.append({"in": {"n": 4, "wells": [3, 7, 2, 9], "pipes": []}})

    # 3. Disconnected pipe clusters (must build at least one well per cluster)
    tests.append({
        "in": {
            "n": 6,
            "wells": [10, 4, 8, 12, 3, 7],
            "pipes": [[1, 2, 1], [2, 3, 2], [4, 5, 2], [5, 6, 1]],
        }
    })

    # 4. Zero-cost wells and pipes
    tests.append({
        "in": {
            "n": 4,
            "wells": [0, 10, 10, 0],
            "pipes": [[1, 2, 0], [2, 3, 5], [3, 4, 0]],
        }
    })

    # 5. Parallel pipes between same houses
    tests.append({
        "in": {
            "n": 4,
            "wells": [10, 10, 10, 10],
            "pipes": [[1, 2, 9], [1, 2, 1], [2, 3, 8], [2, 3, 2], [3, 4, 7], [3, 4, 3]],
        }
    })

    # 6. Connected graph where optimal uses TWO wells instead of expensive bridge pipe
    tests.append({
        "in": {
            "n": 4,
            "wells": [3, 100, 100, 4],
            "pipes": [[1, 2, 1], [2, 3, 50], [3, 4, 1]],
        }
    })

    # 7. All equal costs
    tests.append({
        "in": {
            "n": 5,
            "wells": [5, 5, 5, 5, 5],
            "pipes": [[1, 2, 5], [2, 3, 5], [3, 4, 5], [4, 5, 5], [1, 5, 5]],
        }
    })

    # 8. Maximum cost boundaries
    tests.append({
        "in": {
            "n": 5,
            "wells": [100000, 99999, 100000, 100000, 100000],
            "pipes": [[1, 2, 100000], [2, 3, 99998], [3, 4, 100000], [4, 5, 99997]],
        }
    })

    # 9. Medium random
    rng1 = random.Random(1168)
    n1 = 100
    wells1 = [rng1.randint(10, 500) for _ in range(n1)]
    pipes1 = []
    for _ in range(300):
        u = rng1.randint(1, n1)
        v = rng1.randint(1, n1 - 1)
        if v >= u:
            v += 1
        pipes1.append([u, v, rng1.randint(1, 300)])
    tests.append({"in": {"n": n1, "wells": wells1, "pipes": pipes1}})

    # 10. Larger stress test
    rng2 = random.Random(116802)
    n2 = 750
    wells2 = [rng2.randint(0, 100000) for _ in range(n2)]
    pipes2 = []
    for _ in range(1800):
        u = rng2.randint(1, n2)
        v = rng2.randint(1, n2 - 1)
        if v >= u:
            v += 1
        pipes2.append([u, v, rng2.randint(0, 100000)])
    tests.append({"in": {"n": n2, "wells": wells2, "pipes": pipes2}})

    return tests
