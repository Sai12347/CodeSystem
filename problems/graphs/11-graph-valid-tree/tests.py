import random


def visible():
    return [
        {"in": {"n": 5, "edges": [[0, 1], [0, 2], [0, 3], [1, 4]]}},
        {"in": {"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]}},
        {"in": {"n": 1, "edges": []}},
    ]


def hidden():
    tests = []

    # 1. Two disconnected nodes (0 edges) -> false
    tests.append({"in": {"n": 2, "edges": []}})

    # 2. Two connected nodes -> true
    tests.append({"in": {"n": 2, "edges": [[0, 1]]}})

    # 3. Classic trap: exactly n - 1 edges, but contains a cycle and an isolated node -> false
    tests.append({"in": {"n": 4, "edges": [[0, 1], [1, 2], [2, 0]]}})

    # 4. Forest of two separate trees (acyclic, but disconnected) -> false
    tests.append({"in": {"n": 6, "edges": [[0, 1], [1, 2], [3, 4], [4, 5]]}})

    # 5. Connected graph with one extra edge (cycle of length 4) -> false
    tests.append({"in": {"n": 4, "edges": [[0, 1], [1, 2], [2, 3], [3, 0]]}})

    # 6. Star graph on 10 nodes -> true
    tests.append({"in": {"n": 10, "edges": [[0, i] for i in range(1, 10)]}})

    # 7. Long chain (path graph) on 50 nodes with shuffled edge order -> true
    rng7 = random.Random(2617)
    edges7 = [[i, i + 1] for i in range(49)]
    rng7.shuffle(edges7)
    tests.append({"in": {"n": 50, "edges": edges7}})

    # 8. Two components: component 0..3 has a cycle (4 edges) and component 4..5 has 1 edge -> total 5 == n-1 -> false
    tests.append({"in": {"n": 6, "edges": [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5]]}})

    # 9. Large stress test: random tree with n = 2000 (max constraint) -> true
    rng9 = random.Random(2619)
    n9 = 2000
    perm9 = list(range(n9))
    rng9.shuffle(perm9)
    edges9 = []
    for i in range(1, n9):
        p = rng9.randint(0, i - 1)
        u, v = perm9[p], perm9[i]
        edges9.append([u, v] if rng9.randint(0, 1) == 0 else [v, u])
    rng9.shuffle(edges9)
    tests.append({"in": {"n": n9, "edges": edges9}})

    # 10. Large stress test: n = 2000 with 1999 edges split into a cyclic component + disconnected component -> false
    rng10 = random.Random(2620)
    n10 = 2000
    edges10 = []
    # Component A: 0..1499 as a tree + 1 extra chord (1500 edges)
    for i in range(1, 1500):
        edges10.append([rng10.randint(0, i - 1), i])
    # Add a guaranteed non-duplicate chord in Component A
    seen10 = {(min(u, v), max(u, v)) for u, v in edges10}
    for u in range(100, 1500):
        for v in range(u + 1, 1500):
            if (u, v) not in seen10:
                edges10.append([u, v])
                seen10.add((u, v))
                break
        else:
            continue
        break
    # Component B: 1500..1999 as a tree (499 edges); total edges = 1500 + 499 = 1999 = n - 1
    for i in range(1501, n10):
        edges10.append([rng10.randint(1500, i - 1), i])
    rng10.shuffle(edges10)
    tests.append({"in": {"n": n10, "edges": edges10}})

    return tests
