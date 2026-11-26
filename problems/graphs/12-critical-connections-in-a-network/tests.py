import random


def visible():
    return [
        {"in": {"n": 4, "connections": [[0, 1], [1, 2], [2, 0], [1, 3]]}},
        {"in": {"n": 2, "connections": [[0, 1]]}},
        {"in": {"n": 3, "connections": [[0, 1], [1, 2], [2, 0]]}},
    ]


def hidden():
    tests = []

    # 1. Pure tree (star + chain): every edge is a bridge
    tests.append({"in": {"n": 6, "connections": [[0, 1], [0, 2], [0, 3], [3, 4], [4, 5]]}})

    # 2. Barbell graph: two triangles connected by a single bridge [2, 3]
    tests.append({"in": {"n": 6, "connections": [
        [0, 1], [1, 2], [2, 0],
        [3, 4], [4, 5], [5, 3],
        [2, 3],
    ]}})

    # 3. Complete graph K_5: zero bridges
    k5 = [[u, v] for u in range(5) for v in range(u + 1, 5)]
    tests.append({"in": {"n": 5, "connections": k5}})

    # 4. Figure-eight (two cycles sharing a single articulation vertex, zero bridges)
    tests.append({"in": {"n": 5, "connections": [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]]}})

    # 5. Chain of three triangles linked by two bridges
    tests.append({"in": {"n": 9, "connections": [
        [0, 1], [1, 2], [2, 0],
        [2, 3],
        [3, 4], [4, 5], [5, 3],
        [5, 6],
        [6, 7], [7, 8], [8, 6],
    ]}})

    # 6. Nested/overlapping cycles with dangling bridge tails
    tests.append({"in": {"n": 10, "connections": [
        [0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [1, 3], [2, 4],
        [0, 5], [5, 6],
        [3, 7], [7, 8], [8, 9], [9, 7],
    ]}})

    # 7. Ladder graph (2 x 6 grid): every rung and rail is part of a 4-cycle -> zero bridges
    edges7 = []
    for i in range(6):
        edges7.append([i, i + 6])
        if i + 1 < 6:
            edges7.append([i, i + 1])
            edges7.append([i + 6, i + 7])
    tests.append({"in": {"n": 12, "connections": edges7}})

    # 8. Bridge inside a tree of cycles where DFS start node is deep inside a cycle
    tests.append({"in": {"n": 11, "connections": [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [2, 4], [4, 5],
        [5, 6], [6, 7], [7, 8], [8, 5], [6, 8],
        [7, 9], [9, 10],
    ]}})

    # 9. Stress test: deep chain of 1500 vertices (tests iterative/deep DFS; all 1499 edges are bridges)
    rng9 = random.Random(11929)
    n9 = 1500
    edges9 = [[i, i + 1] for i in range(n9 - 1)]
    rng9.shuffle(edges9)
    tests.append({"in": {"n": n9, "connections": edges9}})

    # 10. Stress test: 20 biconnected clusters of 50 nodes joined by 19 bridges (n = 1000, ~2500 edges)
    rng10 = random.Random(11930)
    clusters = 20
    csize = 50
    n10 = clusters * csize
    edges10 = set()
    for c in range(clusters):
        base = c * csize
        # Cycle covering all nodes in the cluster guarantees biconnectivity (no internal bridges)
        for i in range(csize):
            u = base + i
            v = base + (i + 1) % csize
            edges10.add((min(u, v), max(u, v)))
        # Add random internal chords
        for _ in range(75):
            u = base + rng10.randint(0, csize - 1)
            v = base + rng10.randint(0, csize - 1)
            if u != v:
                edges10.add((min(u, v), max(u, v)))
    # Connect clusters as a random tree -> exactly 19 bridges
    for c in range(1, clusters):
        p = rng10.randint(0, c - 1)
        u = p * csize + rng10.randint(0, csize - 1)
        v = c * csize + rng10.randint(0, csize - 1)
        edges10.add((min(u, v), max(u, v)))
    elist10 = [[u, v] for u, v in edges10]
    rng10.shuffle(elist10)
    tests.append({"in": {"n": n10, "connections": elist10}})

    return tests
