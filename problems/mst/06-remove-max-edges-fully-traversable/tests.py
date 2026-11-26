import random


def visible():
    return [
        {
            "in": {
                "n": 4,
                "edges": [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]],
            }
        },
        {
            "in": {
                "n": 4,
                "edges": [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]],
            }
        },
        {
            "in": {
                "n": 4,
                "edges": [[3, 2, 3], [1, 1, 2], [2, 3, 4]],
            }
        },
    ]


def _gen_traversable(rng, n, extra_edges):
    seen = set()
    edges = []

    def add(t, u, v):
        if u > v:
            u, v = v, u
        key = (t, u, v)
        if key not in seen:
            seen.add(key)
            edges.append([t, u, v])

    # Build a random spanning tree for Alice (using type 1 or 3)
    order1 = list(range(1, n + 1))
    rng.shuffle(order1)
    for i in range(1, n):
        t = 3 if rng.random() < 0.45 else 1
        add(t, order1[i], order1[rng.randrange(i)])

    # Build a random spanning tree for Bob (using type 2 or 3)
    order2 = list(range(1, n + 1))
    rng.shuffle(order2)
    for i in range(1, n):
        t = 3 if rng.random() < 0.3 else 2
        add(t, order2[i], order2[rng.randrange(i)])

    # Add extra redundant edges of all types
    for _ in range(extra_edges):
        u = rng.randint(1, n)
        v = rng.randint(1, n - 1)
        if v >= u:
            v += 1
        add(rng.randint(1, 3), u, v)

    rng.shuffle(edges)
    return edges


def hidden():
    tests = []

    # 1. Single node, no edges
    tests.append({"in": {"n": 1, "edges": []}})

    # 2. Two nodes with all 3 edge types (keep type 3, remove type 1 and type 2)
    tests.append({"in": {"n": 2, "edges": [[1, 1, 2], [2, 1, 2], [3, 1, 2]]}})

    # 3. Only Type 3 edges forming complete K5
    k5_t3 = [[3, i, j] for i in range(1, 6) for j in range(i + 1, 6)]
    tests.append({"in": {"n": 5, "edges": k5_t3}})

    # 4. Only Type 1 and Type 2 edges (no Type 3), both connected with extra edges
    tests.append({
        "in": {
            "n": 4,
            "edges": [
                [1, 1, 2], [1, 2, 3], [1, 3, 4], [1, 1, 4],
                [2, 1, 3], [2, 2, 4], [2, 1, 2], [2, 3, 4],
            ],
        }
    })

    # 5. Alice fully connected, Bob disconnected -> -1
    tests.append({
        "in": {
            "n": 4,
            "edges": [[1, 1, 2], [1, 2, 3], [1, 3, 4], [2, 1, 2], [2, 3, 4]],
        }
    })

    # 6. Bob fully connected, Alice disconnected -> -1
    tests.append({
        "in": {
            "n": 4,
            "edges": [[2, 1, 2], [2, 2, 3], [2, 3, 4], [3, 1, 2], [1, 3, 4]],
        }
    })

    # 7. Redundant Type 3 cycle + needed Type 1 and Type 2 bridges
    tests.append({
        "in": {
            "n": 6,
            "edges": [
                [3, 1, 2], [3, 2, 3], [3, 1, 3],
                [3, 4, 5], [3, 5, 6], [3, 4, 6],
                [1, 3, 4], [1, 1, 6],
                [2, 2, 5], [2, 3, 6],
            ],
        }
    })

    # 8. Order-dependent trap: Type 1 and Type 2 edges appear BEFORE Type 3 edges
    tests.append({
        "in": {
            "n": 5,
            "edges": [
                [1, 1, 2], [1, 2, 3], [1, 3, 4], [1, 4, 5],
                [2, 1, 2], [2, 2, 3], [2, 3, 4], [2, 4, 5],
                [3, 1, 2], [3, 2, 3], [3, 3, 4], [3, 4, 5],
            ],
        }
    })

    # 9. Medium random traversable graph
    rng1 = random.Random(1579)
    tests.append({"in": {"n": 100, "edges": _gen_traversable(rng1, 100, 200)}})

    # 10. Larger stress test
    rng2 = random.Random(157902)
    tests.append({"in": {"n": 750, "edges": _gen_traversable(rng2, 750, 900)}})

    return tests
