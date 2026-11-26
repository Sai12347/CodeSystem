import random


def _from_edges(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    return [sorted(s) for s in adj]


def visible():
    return [
        {"in": {"graph": [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]}},
        {"in": {"graph": [[1, 3], [0, 2], [1, 3], [0, 2]]}},
        {"in": {"graph": [[]]}},
    ]


def hidden():
    tests = []

    # 1. Multiple isolated nodes (edgeless graph -> bipartite)
    tests.append({"in": {"graph": [[], [], [], []]}})

    # 2. Minimal 2-node connected graph
    tests.append({"in": {"graph": [[1], [0]]}})

    # 3. Odd cycle C_5 -> false
    tests.append({"in": {"graph": _from_edges(5, [(i, (i + 1) % 5) for i in range(5)])}})

    # 4. Even cycle C_6 -> true
    tests.append({"in": {"graph": _from_edges(6, [(i, (i + 1) % 6) for i in range(6)])}})

    # 5. Disconnected: bipartite component + isolated node + odd cycle component -> false
    edges5 = [(0, 1), (1, 2), (2, 3), (3, 0), (5, 6), (6, 7), (7, 5)]
    tests.append({"in": {"graph": _from_edges(8, edges5)}})

    # 6. Disconnected: multiple bipartite components (tree + even cycle + isolated nodes) -> true
    edges6 = [(0, 1), (0, 2), (1, 3), (1, 4), (5, 6), (6, 7), (7, 8), (8, 5), (10, 11)]
    tests.append({"in": {"graph": _from_edges(12, edges6)}})

    # 7. Complete bipartite graph K_{4,5} -> true
    edges7 = [(u, 4 + v) for u in range(4) for v in range(5)]
    tests.append({"in": {"graph": _from_edges(9, edges7)}})

    # 8. Complete graph K_5 -> false
    edges8 = [(u, v) for u in range(5) for v in range(u + 1, 5)]
    tests.append({"in": {"graph": _from_edges(5, edges8)}})

    # 9. Stress test: random bipartite graph (n = 400, ~1200 edges) -> true
    rng1 = random.Random(7851)
    n9 = 400
    part = [rng1.randint(0, 1) for _ in range(n9)]
    left = [i for i in range(n9) if part[i] == 0]
    right = [i for i in range(n9) if part[i] == 1]
    edges9 = set()
    for _ in range(1200):
        u = rng1.choice(left)
        v = rng1.choice(right)
        edges9.add((min(u, v), max(u, v)))
    tests.append({"in": {"graph": _from_edges(n9, edges9)}})

    # 10. Stress test: connected bipartite graph (n = 400) + 1 same-side edge creating a deep odd cycle -> false
    rng2 = random.Random(7852)
    n10 = 400
    order = list(range(n10))
    rng2.shuffle(order)
    edges10 = set()
    # Spanning chain alternating partitions ensures connectivity
    for i in range(n10 - 1):
        u, v = order[i], order[i + 1]
        edges10.add((min(u, v), max(u, v)))
    evens = [order[i] for i in range(0, n10, 2)]
    odds = [order[i] for i in range(1, n10, 2)]
    for _ in range(800):
        u = rng2.choice(evens)
        v = rng2.choice(odds)
        edges10.add((min(u, v), max(u, v)))
    # Inject a single edge between two vertices in the same partition
    u, v = evens[10], evens[150]
    edges10.add((min(u, v), max(u, v)))
    tests.append({"in": {"graph": _from_edges(n10, edges10)}})

    return tests
