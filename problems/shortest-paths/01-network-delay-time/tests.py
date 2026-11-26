import random


def visible():
    return [
        {"in": {"times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]], "n": 4, "k": 2}},
        {"in": {"times": [[1, 2, 1]], "n": 2, "k": 1}},
        {"in": {"times": [[1, 2, 1]], "n": 2, "k": 2}},
    ]


def hidden():
    tests = []

    # 1. Single node, no edges
    tests.append({"in": {"times": [], "n": 1, "k": 1}})

    # 2. Zero-weight edge
    tests.append({"in": {"times": [[1, 2, 0]], "n": 2, "k": 1}})

    # 3. Disconnected graph with an isolated node
    tests.append({"in": {
        "times": [[1, 2, 3], [2, 3, 4], [3, 4, 2], [4, 1, 1]],
        "n": 5,
        "k": 1,
    }})

    # 4. Multi-hop cheaper path beats expensive direct edge (BFS trap)
    tests.append({"in": {
        "times": [[1, 2, 10], [1, 3, 1], [3, 4, 1], [4, 2, 1], [2, 5, 2]],
        "n": 5,
        "k": 1,
    }})

    # 5. Zero-weight cycle plus positive tail
    tests.append({"in": {
        "times": [[1, 2, 0], [2, 3, 0], [3, 1, 0], [3, 4, 5], [4, 5, 0]],
        "n": 5,
        "k": 1,
    }})

    # 6. Diamond with equal-cost shortest paths and reverse edges
    tests.append({"in": {
        "times": [
            [1, 2, 4], [1, 3, 2], [3, 2, 2], [2, 4, 3],
            [3, 4, 5], [4, 1, 1], [2, 5, 1], [4, 5, 1],
        ],
        "n": 5,
        "k": 1,
    }})

    # 7. Reverse linear chain from n down to 1
    chain = [[i, i - 1, i] for i in range(10, 1, -1)]
    tests.append({"in": {"times": chain, "n": 10, "k": 10}})

    # 8. Star graph with max weight 100
    star = [[1, v, 100] for v in range(2, 16)]
    tests.append({"in": {"times": star, "n": 15, "k": 1}})

    # 9. Medium random directed graph (n = 40)
    rng = random.Random(7431)
    n9 = 40
    edges9 = {}
    for v in range(2, n9 + 1):
        u = rng.randint(1, v - 1)
        edges9[(u, v)] = rng.randint(0, 100)
    for _ in range(360):
        u = rng.randint(1, n9)
        v = rng.randint(1, n9)
        if u != v and (u, v) not in edges9:
            edges9[(u, v)] = rng.randint(0, 100)
    tests.append({"in": {
        "times": [[u, v, w] for (u, v), w in sorted(edges9.items())],
        "n": n9,
        "k": 1,
    }})

    # 10. Stress test: dense random graph (n = 100, ~1200 edges)
    rng2 = random.Random(7432)
    n10 = 100
    edges10 = {}
    order = list(range(1, n10 + 1))
    rng2.shuffle(order)
    for i in range(1, n10):
        u = order[rng2.randint(0, i - 1)]
        v = order[i]
        edges10[(u, v)] = rng2.randint(1, 100)
    for _ in range(1200):
        u = rng2.randint(1, n10)
        v = rng2.randint(1, n10)
        if u != v and (u, v) not in edges10:
            edges10[(u, v)] = rng2.randint(0, 100)
    tests.append({"in": {
        "times": [[u, v, w] for (u, v), w in sorted(edges10.items())],
        "n": n10,
        "k": order[0],
    }})

    return tests
