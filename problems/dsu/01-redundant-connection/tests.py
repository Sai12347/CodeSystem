import random


def _gen_tree_plus_one(n: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    nodes = list(range(1, n + 1))
    rng.shuffle(nodes)
    edges = []
    seen = set()
    for i in range(1, n):
        u = nodes[i]
        v = nodes[rng.randrange(i)]
        a, b = (u, v) if u < v else (v, u)
        edges.append([a, b])
        seen.add((a, b))
    while True:
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u != v:
            a, b = (u, v) if u < v else (v, u)
            if (a, b) not in seen:
                edges.append([a, b])
                break
    rng.shuffle(edges)
    return edges


def visible():
    return [
        {"in": {"edges": [[1, 2], [1, 3], [2, 3]]}},
        {"in": {"edges": [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]}},
    ]


def hidden():
    # 1. Minimum n=3 triangle in reverse order
    t1 = [[2, 3], [1, 3], [1, 2]]
    # 2. Cycle formed early, followed by a long tail of tree edges
    t2 = [[1, 2], [2, 3], [1, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]]
    # 3. Single full-graph cycle of length 10 with closing edge in the middle
    t3 = [[1, 2], [2, 3], [3, 4], [4, 5], [1, 10], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]
    # 4. Star centered at 1 plus one extra edge between leaves
    t4 = [[1, i] for i in range(2, 12)] + [[5, 9]]
    # 5. Two subtrees connected by a bridge plus a cross-edge forming a big cycle
    t5 = [
        [1, 2], [1, 3], [2, 4], [2, 5],
        [6, 7], [6, 8], [7, 9], [7, 10],
        [3, 6], [5, 10],
    ]
    # 6. Cycle strictly on highest-numbered nodes with a path attached
    t6 = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [7, 10]]
    # 7. Binary tree of 15 nodes plus chord between two deep leaves
    t7 = [[i, 2 * i] for i in range(1, 8)] + [[i, 2 * i + 1] for i in range(1, 8)]
    t7.insert(10, [8, 15])
    # 8. Cycle spanning nodes 2..6 in reverse insertion order
    t8 = [[5, 6], [4, 5], [3, 4], [2, 3], [2, 6], [1, 2], [6, 7]]
    # 9. Medium random tree + 1 edge (n = 200)
    t9 = _gen_tree_plus_one(200, 6841)
    # 10. Max-size stress test (n = 1000)
    t10 = _gen_tree_plus_one(1000, 6842)

    return [{"in": {"edges": t}} for t in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
