import random


def visible():
    return [
        {"in": {
            "n": 4,
            "flights": [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
            "src": 0, "dst": 3, "k": 1,
        }},
        {"in": {
            "n": 3,
            "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
            "src": 0, "dst": 2, "k": 1,
        }},
        {"in": {
            "n": 3,
            "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
            "src": 0, "dst": 2, "k": 0,
        }},
    ]


def hidden():
    tests = []

    # 1. Empty flights list
    tests.append({"in": {"n": 2, "flights": [], "src": 0, "dst": 1, "k": 0}})

    # 2. Minimum graph with direct flight
    tests.append({"in": {"n": 2, "flights": [[0, 1, 42]], "src": 0, "dst": 1, "k": 0}})

    # 3. Chain where k is 1 stop too small
    tests.append({"in": {
        "n": 5,
        "flights": [[0, 1, 10], [1, 2, 10], [2, 3, 10], [3, 4, 10]],
        "src": 0, "dst": 4, "k": 2,
    }})

    # 4. Same chain where k is exact boundary (3 stops = 4 edges)
    tests.append({"in": {
        "n": 5,
        "flights": [[0, 1, 10], [1, 2, 10], [2, 3, 10], [3, 4, 10]],
        "src": 0, "dst": 4, "k": 3,
    }})

    # 5. Classic Dijkstra-trap: cheaper path to node 3 uses 2 edges, pricier uses 1 edge,
    #    and only the 1-edge arrival can still reach dst within k=2 stops.
    tests.append({"in": {
        "n": 6,
        "flights": [
            [0, 1, 1], [1, 2, 1], [2, 3, 1],   # 0->1->2->3: cost 3, 3 edges
            [0, 3, 10],                         # 0->3: cost 10, 1 edge
            [3, 4, 5], [4, 5, 5],               # 3->4->5: cost 10, 2 edges
        ],
        "src": 0, "dst": 5, "k": 2,
    }})

    # 6. Graph with cycles and large k
    tests.append({"in": {
        "n": 6,
        "flights": [
            [0, 1, 2], [1, 2, 2], [2, 0, 1],
            [2, 3, 5], [3, 1, 1], [3, 4, 7], [4, 5, 3], [1, 5, 50],
        ],
        "src": 0, "dst": 5, "k": 5,
    }})

    # 7. Unreachable destination even with max k = n - 1
    tests.append({"in": {
        "n": 6,
        "flights": [[0, 1, 5], [1, 2, 5], [2, 0, 5], [3, 4, 5], [4, 5, 5]],
        "src": 0, "dst": 5, "k": 5,
    }})

    # 8. Max edge prices boundary (price = 10000)
    max_chain = [[i, i + 1, 10000] for i in range(20)]
    tests.append({"in": {
        "n": 21,
        "flights": max_chain,
        "src": 0, "dst": 20, "k": 19,
    }})

    # 9. Medium random directed graph (n = 40, k = 4)
    rng = random.Random(7871)
    n9 = 40
    e9 = {}
    for _ in range(300):
        u = rng.randint(0, n9 - 1)
        v = rng.randint(0, n9 - 1)
        if u != v and (u, v) not in e9:
            e9[(u, v)] = rng.randint(1, 5000)
    tests.append({"in": {
        "n": n9,
        "flights": [[u, v, p] for (u, v), p in sorted(e9.items())],
        "src": 0, "dst": n9 - 1, "k": 4,
    }})

    # 10. Stress test: larger directed graph (n = 100, ~900 flights, k = 12)
    rng2 = random.Random(7872)
    n10 = 100
    e10 = {}
    for i in range(n10 - 1):
        e10[(i, i + 1)] = rng2.randint(500, 2000)
    for _ in range(900):
        u = rng2.randint(0, n10 - 1)
        v = rng2.randint(0, n10 - 1)
        if u != v and (u, v) not in e10:
            e10[(u, v)] = rng2.randint(1, 10000)
    tests.append({"in": {
        "n": n10,
        "flights": [[u, v, p] for (u, v), p in sorted(e10.items())],
        "src": 0, "dst": n10 - 1, "k": 12,
    }})

    return tests
