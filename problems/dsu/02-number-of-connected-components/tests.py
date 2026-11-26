import random


def _gen_random_graph(n: int, m: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    seen = set()
    edges = []
    while len(edges) < m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        if u > v:
            u, v = v, u
        if (u, v) not in seen:
            seen.add((u, v))
            edges.append([u, v])
    return edges


def visible():
    return [
        {"in": {"n": 5, "edges": [[0, 1], [1, 2], [3, 4]]}},
        {"in": {"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]}},
    ]


def hidden():
    # 1. Minimum single isolated node
    t1 = (1, [])
    # 2. All isolated nodes
    t2 = (10, [])
    # 3. Complete graph K_6
    t3 = (6, [[i, j] for i in range(6) for j in range(i + 1, 6)])
    # 4. Disconnected cycles + isolated nodes
    t4 = (12, [[0, 1], [1, 2], [0, 2], [3, 4], [4, 5], [3, 5], [6, 7], [7, 8], [8, 9], [6, 9]])
    # 5. Ten disjoint pairs
    t5 = (20, [[2 * i, 2 * i + 1] for i in range(10)])
    # 6. Chain added in reverse order with extra cycle edges
    t6 = (10, [[i, i + 1] for i in range(8, -1, -1)] + [[0, 9], [2, 7], [3, 6]])
    # 7. Two cliques bridged by a single edge at the end
    c1 = [[i, j] for i in range(5) for j in range(i + 1, 5)]
    c2 = [[i, j] for i in range(5, 10) for j in range(i + 1, 10)]
    t7 = (10, c1 + c2 + [[4, 5]])
    # 8. Three star graphs of varying sizes
    t8 = (
        15,
        [[0, i] for i in range(1, 5)]
        + [[5, i] for i in range(6, 11)]
        + [[11, i] for i in range(12, 15)],
    )
    # 9. Medium random sparse graph
    t9 = (400, _gen_random_graph(400, 350, 3231))
    # 10. Stress test: n = 2000, m = 3000
    t10 = (2000, _gen_random_graph(2000, 3000, 3232))

    return [{"in": {"n": n, "edges": edges}} for n, edges in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
