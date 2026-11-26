import random


def visible():
    return [
        {"in": {"n": 4, "edges": [[0, 1, 4], [0, 2, 3], [1, 2, 1], [1, 3, 2], [2, 3, 5]]}},
        {"in": {"n": 4, "edges": [[0, 1, 2], [2, 3, 5]]}},
        {"in": {"n": 3, "edges": [[0, 0, 1], [0, 1, 10], [0, 1, 3], [1, 2, 4], [0, 2, 8]]}},
    ]


def _gen_connected(rng, n, extra_edges, max_w):
    edges = []
    order = list(range(n))
    rng.shuffle(order)
    for i in range(1, n):
        u = order[i]
        v = order[rng.randrange(i)]
        edges.append([u, v, rng.randint(0, max_w)])
    for _ in range(extra_edges):
        u = rng.randrange(n)
        v = rng.randrange(n)
        edges.append([u, v, rng.randint(0, max_w)])
    rng.shuffle(edges)
    return edges


def hidden():
    tests = []

    # 1. Single vertex with self-loops (must return 0)
    tests.append({"in": {"n": 1, "edges": [[0, 0, 5], [0, 0, 0]]}})

    # 2. Single vertex with no edges
    tests.append({"in": {"n": 1, "edges": []}})

    # 3. Two vertices, no edges (disconnected)
    tests.append({"in": {"n": 2, "edges": []}})

    # 4. 64-bit integer overflow boundary (sum = 4 * 10^9 > 2^31 - 1)
    tests.append({
        "in": {
            "n": 5,
            "edges": [
                [0, 1, 1000000000], [1, 2, 1000000000],
                [2, 3, 1000000000], [3, 4, 1000000000],
                [0, 4, 1000000000],
            ],
        }
    })

    # 5. Zero-weight spanning tree with heavier alternative edges
    tests.append({
        "in": {
            "n": 5,
            "edges": [[0, 1, 0], [1, 2, 0], [2, 3, 0], [3, 4, 0], [0, 4, 100], [1, 3, 50]],
        }
    })

    # 6. Star from 0 with expensive spokes vs cheap outer ring (tests Prim heap updates)
    tests.append({
        "in": {
            "n": 6,
            "edges": [
                [0, 1, 100], [0, 2, 90], [0, 3, 80], [0, 4, 70], [0, 5, 10],
                [5, 4, 1], [4, 3, 1], [3, 2, 1], [2, 1, 1],
            ],
        }
    })

    # 7. Dense component on 0..3 plus isolated vertex 4 having only self-loops
    tests.append({
        "in": {
            "n": 5,
            "edges": [
                [0, 1, 1], [0, 2, 2], [0, 3, 3], [1, 2, 1], [1, 3, 2], [2, 3, 1],
                [4, 4, 0], [4, 4, 7],
            ],
        }
    })

    # 8. Reverse-sorted parallel edges
    tests.append({
        "in": {
            "n": 4,
            "edges": [
                [0, 1, 50], [0, 1, 20], [0, 1, 5],
                [1, 2, 40], [1, 2, 15], [1, 2, 3],
                [2, 3, 30], [2, 3, 10], [2, 3, 2],
            ],
        }
    })

    # 9. Medium random with large weights & self-loops/parallels
    rng1 = random.Random(5050)
    tests.append({"in": {"n": 120, "edges": _gen_connected(rng1, 120, 350, 1000000000)}})

    # 10. Larger stress test with 64-bit weights
    rng2 = random.Random(505002)
    tests.append({"in": {"n": 700, "edges": _gen_connected(rng2, 700, 1500, 1000000000)}})

    return tests
