import random


def _edges_to_adj(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u - 1].add(v)
            adj[v - 1].add(u)
    return [sorted(s) for s in adj]


def visible():
    return [
        {"in": {"adjList": [[2, 4], [1, 3], [2, 4], [1, 3]]}},
        {"in": {"adjList": [[]]}},
        {"in": {"adjList": []}},
    ]


def hidden():
    tests = []

    # 1. Two connected nodes
    tests.append({"in": {"adjList": [[2], [1]]}})

    # 2. Triangle K3
    tests.append({"in": {"adjList": [[2, 3], [1, 3], [1, 2]]}})

    # 3. Complete graph K5
    k5_edges = [(i, j) for i in range(1, 6) for j in range(i + 1, 6)]
    tests.append({"in": {"adjList": _edges_to_adj(5, k5_edges)}})

    # 4. Star graph (node 1 connected to 2..15)
    star_edges = [(1, i) for i in range(2, 16)]
    tests.append({"in": {"adjList": _edges_to_adj(15, star_edges)}})

    # 5. Path graph of 20 nodes
    path_edges = [(i, i + 1) for i in range(1, 20)]
    tests.append({"in": {"adjList": _edges_to_adj(20, path_edges)}})

    # 6. Cycle of 15 nodes
    cycle_edges = [(i, i + 1) for i in range(1, 15)] + [(15, 1)]
    tests.append({"in": {"adjList": _edges_to_adj(15, cycle_edges)}})

    # 7. Barbell graph (two K4 cliques joined by a bridge)
    barbell = []
    for i in range(1, 5):
        for j in range(i + 1, 5):
            barbell.append((i, j))
    for i in range(5, 9):
        for j in range(i + 1, 9):
            barbell.append((i, j))
    barbell.append((4, 5))
    tests.append({"in": {"adjList": _edges_to_adj(8, barbell)}})

    # 8. Complete binary tree (15 nodes)
    tree_edges = [(i, 2 * i) for i in range(1, 8)] + [(i, 2 * i + 1) for i in range(1, 8)]
    tests.append({"in": {"adjList": _edges_to_adj(15, tree_edges)}})

    # 9. 5x5 grid graph (25 nodes, many overlapping 4-cycles)
    grid_edges = []
    for r in range(5):
        for c in range(5):
            u = r * 5 + c + 1
            if r + 1 < 5:
                grid_edges.append((u, (r + 1) * 5 + c + 1))
            if c + 1 < 5:
                grid_edges.append((u, r * 5 + (c + 1) + 1))
    tests.append({"in": {"adjList": _edges_to_adj(25, grid_edges)}})

    # 10. Max-constraint 100-node connected graph (spanning tree + extra random edges)
    rng = random.Random(1331)
    n = 100
    edges = []
    for i in range(2, n + 1):
        p = rng.randint(1, i - 1)
        edges.append((p, i))
    for _ in range(350):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u != v:
            edges.append((u, v))
    tests.append({"in": {"adjList": _edges_to_adj(n, edges)}})

    return tests
