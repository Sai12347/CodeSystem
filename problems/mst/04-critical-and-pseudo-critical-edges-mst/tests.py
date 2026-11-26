import random


def visible():
    return [
        {
            "in": {
                "n": 5,
                "edges": [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]],
            }
        },
        {
            "in": {
                "n": 4,
                "edges": [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]],
            }
        },
        {
            "in": {
                "n": 3,
                "edges": [[0, 1, 1], [1, 2, 2], [0, 2, 5]],
            }
        },
    ]


def _gen_simple_connected(rng, n, m, max_w):
    used = set()
    edges = []
    order = list(range(n))
    rng.shuffle(order)
    for i in range(1, n):
        u, v = order[i], order[rng.randrange(i)]
        if u > v:
            u, v = v, u
        used.add((u, v))
        edges.append([u, v, rng.randint(1, max_w)])
    while len(edges) < m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        if u > v:
            u, v = v, u
        if (u, v) not in used:
            used.add((u, v))
            edges.append([u, v, rng.randint(1, max_w)])
    rng.shuffle(edges)
    return edges


def hidden():
    tests = []

    # 1. Minimum graph: 2 vertices, 1 edge
    tests.append({"in": {"n": 2, "edges": [[0, 1, 10]]}})

    # 2. Pure tree (every edge is critical)
    tests.append({
        "in": {
            "n": 6,
            "edges": [[0, 1, 5], [1, 2, 2], [1, 3, 8], [3, 4, 1], [3, 5, 4]],
        }
    })

    # 3. Complete graph K4 with all equal weights (all pseudo-critical)
    k4 = [[i, j, 5] for i in range(4) for j in range(i + 1, 4)]
    tests.append({"in": {"n": 4, "edges": k4}})

    # 4. Unique MST plus heavy redundant chords
    tests.append({
        "in": {
            "n": 5,
            "edges": [
                [0, 1, 1], [1, 2, 2], [2, 3, 3], [3, 4, 4],
                [0, 2, 10], [0, 3, 11], [0, 4, 12], [1, 3, 13], [1, 4, 14], [2, 4, 15],
            ],
        }
    })

    # 5. Critical bridge connecting two equal-weight triangles
    tests.append({
        "in": {
            "n": 6,
            "edges": [
                [0, 1, 2], [1, 2, 2], [0, 2, 2],
                [2, 3, 100],
                [3, 4, 3], [4, 5, 3], [3, 5, 3],
            ],
        }
    })

    # 6. Tricky equal-weight non-MST edge: edge (0,2,2) has weight 2 (same as an MST edge 2-3),
    # but forms a cycle with strictly lighter edges (0,1,1) and (1,2,1), so it is NEVER in any MST!
    tests.append({
        "in": {
            "n": 4,
            "edges": [[0, 1, 1], [1, 2, 1], [0, 2, 2], [2, 3, 2], [0, 3, 2]],
        }
    })

    # 7. Two equal-weight cycles sharing a vertex plus a heavy diagonal
    tests.append({
        "in": {
            "n": 7,
            "edges": [
                [0, 1, 4], [1, 2, 4], [2, 3, 4], [0, 3, 4],
                [3, 4, 7], [4, 5, 7], [5, 6, 7], [3, 6, 7],
                [0, 6, 1000],
            ],
        }
    })

    # 8. Reverse-ordered weights and indices (verifies sorted output order)
    tests.append({
        "in": {
            "n": 5,
            "edges": [
                [3, 4, 10], [2, 4, 10], [1, 4, 5], [2, 3, 5],
                [0, 3, 3], [1, 2, 2], [0, 1, 1],
            ],
        }
    })

    # 9. Medium random with small weight domain (rich mix of critical, pseudo-critical, unused)
    rng1 = random.Random(1489)
    tests.append({"in": {"n": 25, "edges": _gen_simple_connected(rng1, 25, 80, 6)}})

    # 10. Stress test near max constraints (n = 80, m = 195)
    rng2 = random.Random(148902)
    tests.append({"in": {"n": 80, "edges": _gen_simple_connected(rng2, 80, 195, 8)}})

    return tests
