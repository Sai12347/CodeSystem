import random


def visible():
    return [
        {"in": {"n": 3, "connections": [[1, 2, 5], [1, 3, 6], [2, 3, 1]]}},
        {"in": {"n": 4, "connections": [[1, 2, 3], [3, 4, 4]]}},
        {"in": {"n": 4, "connections": [[1, 2, 1], [2, 3, 2], [3, 4, 3], [1, 4, 10], [1, 3, 2]]}},
    ]


def _gen_connected_graph(rng, n, extra_edges, max_cost):
    edges = []
    # Random spanning tree first so graph is guaranteed connected
    order = list(range(1, n + 1))
    rng.shuffle(order)
    for i in range(1, n):
        u = order[i]
        v = order[rng.randrange(i)]
        edges.append([u, v, rng.randint(0, max_cost)])
    for _ in range(extra_edges):
        u = rng.randint(1, n)
        v = rng.randint(1, n - 1)
        if v >= u:
            v += 1
        edges.append([u, v, rng.randint(0, max_cost)])
    rng.shuffle(edges)
    return edges


def hidden():
    tests = []

    # 1. Single city, no connections
    tests.append({"in": {"n": 1, "connections": []}})

    # 2. Two cities, empty connections -> impossible
    tests.append({"in": {"n": 2, "connections": []}})

    # 3. Parallel / duplicate edges between same cities
    tests.append({
        "in": {
            "n": 3,
            "connections": [[1, 2, 10], [1, 2, 2], [2, 3, 8], [2, 3, 3], [1, 3, 1], [1, 3, 1]],
        }
    })

    # 4. Zero-cost edges
    tests.append({
        "in": {
            "n": 4,
            "connections": [[1, 2, 0], [2, 3, 0], [3, 4, 0], [1, 4, 5], [1, 3, 2]],
        }
    })

    # 5. All equal weights with dense cycles (K5)
    k5 = [[i, j, 7] for i in range(1, 6) for j in range(i + 1, 6)]
    tests.append({"in": {"n": 5, "connections": k5}})

    # 6. Disconnected: complete K4 plus isolated city 5
    k4 = [[i, j, i + j] for i in range(1, 5) for j in range(i + 1, 5)]
    tests.append({"in": {"n": 5, "connections": k4}})

    # 7. Reverse-sorted chain plus cheaper shortcuts
    chain_rev = [[i, i + 1, 100 - i * 10] for i in range(1, 8)] + [[1, 8, 1], [2, 7, 2], [3, 6, 3], [4, 5, 4]]
    tests.append({"in": {"n": 8, "connections": chain_rev}})

    # 8. Maximum cost boundary
    tests.append({
        "in": {
            "n": 5,
            "connections": [[1, 2, 100000], [2, 3, 100000], [3, 4, 100000], [4, 5, 100000], [1, 5, 99999]],
        }
    })

    # 9. Medium random connected graph
    rng1 = random.Random(1135)
    tests.append({"in": {"n": 100, "connections": _gen_connected_graph(rng1, 100, 300, 5000)}})

    # 10. Larger stress test (connected)
    rng2 = random.Random(113502)
    tests.append({"in": {"n": 900, "connections": _gen_connected_graph(rng2, 900, 1600, 100000)}})

    return tests
