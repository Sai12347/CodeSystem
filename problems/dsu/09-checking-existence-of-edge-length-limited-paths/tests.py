import random


def _gen_instance(n: int, e_cnt: int, q_cnt: int, max_w: int, seed: int):
    rng = random.Random(seed)
    edges = []
    for _ in range(e_cnt):
        u = rng.randrange(n)
        v = rng.randrange(n)
        while v == u:
            v = rng.randrange(n)
        w = rng.randint(1, max_w)
        edges.append([u, v, w])
    queries = []
    for _ in range(q_cnt):
        p = rng.randrange(n)
        q = rng.randrange(n)
        while q == p:
            q = rng.randrange(n)
        lim = rng.randint(1, max_w)
        queries.append([p, q, lim])
    return n, edges, queries


def visible():
    return [
        {
            "in": {
                "n": 3,
                "edgeList": [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]],
                "queries": [[0, 1, 2], [0, 2, 5]],
            }
        },
        {
            "in": {
                "n": 5,
                "edgeList": [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]],
                "queries": [[0, 4, 14], [1, 4, 13]],
            }
        },
    ]


def hidden():
    # 1. Minimum n=2, strict inequality boundary checks
    t1 = (2, [[0, 1, 5]], [[0, 1, 1], [0, 1, 5], [0, 1, 6], [1, 0, 5], [1, 0, 1000000000]])
    # 2. Multiple parallel edges between the same pair with different weights
    t2 = (
        3,
        [[0, 1, 1000000000], [0, 1, 500], [1, 0, 10], [1, 2, 100], [1, 2, 20]],
        [[0, 1, 10], [0, 1, 11], [0, 2, 20], [0, 2, 21], [2, 0, 1000000000]],
    )
    # 3. Max weight 10^9 boundary (tests overflow and strict < comparison)
    t3 = (
        4,
        [[0, 1, 1000000000], [1, 2, 999999999], [2, 3, 1]],
        [[0, 1, 1000000000], [1, 2, 1000000000], [1, 3, 1000000000], [0, 3, 1000000000], [2, 3, 2]],
    )
    # 4. Disconnected graph components
    t4 = (
        6,
        [[0, 1, 3], [1, 2, 4], [3, 4, 2], [4, 5, 1]],
        [[0, 2, 5], [3, 5, 3], [0, 3, 1000000000], [2, 5, 1000000000], [1, 4, 100]],
    )
    # 5. Queries given in strictly descending limit order
    t5 = (
        6,
        [[0, 1, 10], [1, 2, 20], [2, 3, 30], [3, 4, 40], [4, 5, 50]],
        [[0, 5, 100], [0, 5, 51], [0, 5, 50], [0, 4, 41], [0, 4, 40], [0, 3, 31], [0, 2, 21], [0, 1, 11], [0, 1, 10]],
    )
    # 6. Duplicate queries and equal limit values
    t6 = (
        5,
        [[0, 1, 7], [1, 2, 7], [2, 3, 7], [3, 4, 8]],
        [[0, 3, 8], [0, 3, 8], [0, 4, 8], [0, 4, 9], [1, 3, 7], [1, 3, 8]],
    )
    # 7. Indirect cheap detour beats direct expensive edge
    t7 = (
        5,
        [[0, 4, 1000], [0, 1, 5], [1, 2, 6], [2, 3, 7], [3, 4, 8]],
        [[0, 4, 8], [0, 4, 9], [0, 4, 1000], [0, 4, 1001], [1, 4, 9]],
    )
    # 8. Large n = 100000 sparse graph (verifies O(n) memory and no O(n^2) behavior)
    rng8 = random.Random(16970)
    chain_nodes = [0, 1, 50000, 99998, 99999] + [rng8.randint(2, 99997) for _ in range(200)]
    edges8 = []
    for i in range(len(chain_nodes) - 1):
        u, v = chain_nodes[i], chain_nodes[i + 1]
        if u != v:
            edges8.append([u, v, rng8.randint(1, 500)])
    queries8 = [
        [0, 99999, 501],
        [0, 99999, 250],
        [0, 50000, 501],
        [1, 99998, 100],
        [42, 99999, 1000000000],
    ]
    for _ in range(100):
        a = rng8.choice(chain_nodes)
        b = rng8.choice(chain_nodes)
        if a == b:
            b = (a + 1) % 100000
        queries8.append([a, b, rng8.randint(1, 550)])
    t8 = (100000, edges8, queries8)
    # 9. Medium random graph
    t9 = _gen_instance(200, 400, 300, 5000, 16971)
    # 10. Stress test: n = 1500, E = 1500, Q = 1000
    t10 = _gen_instance(1500, 1500, 1000, 1000000000, 16972)

    return [
        {"in": {"n": n, "edgeList": el, "queries": qs}}
        for n, el, qs in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)
    ]
