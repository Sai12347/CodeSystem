import random


def _gen_stones(n: int, max_coord: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    seen = set()
    res = []
    while len(res) < n:
        x = rng.randint(0, max_coord)
        y = rng.randint(0, max_coord)
        if (x, y) not in seen:
            seen.add((x, y))
            res.append([x, y])
    return res


def visible():
    return [
        {"in": {"stones": [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]}},
        {"in": {"stones": [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]}},
        {"in": {"stones": [[0, 0]]}},
    ]


def hidden():
    # 1. Two completely independent stones on diagonal
    t1 = [[0, 0], [1, 1]]
    # 2. All stones on the same row
    t2 = [[5, 0], [5, 3], [5, 7], [5, 100], [5, 10000]]
    # 3. All stones on the same column
    t3 = [[0, 9], [2, 9], [5, 9], [9999, 9], [10000, 9]]
    # 4. Staircase chain connecting (0,0) through (9,9)
    t4 = [[i, i] for i in range(10)] + [[i, i + 1] for i in range(9)]
    # 5. Boundary coordinates 0 and 10000 (tests row/col offset collision bugs)
    t5 = [[0, 10000], [10000, 0], [10000, 10000], [0, 0], [5000, 5000]]
    # 6. Multiple disjoint components + isolated stones
    t6 = [
        [0, 0], [0, 1], [1, 1],
        [3, 3], [3, 4], [4, 4], [4, 3],
        [7, 7],
        [8, 9],
        [10, 10], [10, 12],
    ]
    # 7. Two components bridged by the very last stone
    t7 = [[0, 0], [0, 1], [1, 0], [5, 5], [5, 6], [6, 5], [1, 6]]
    # 8. Dense 10 x 10 grid of 100 stones
    t8 = [[r, c] for r in range(10) for c in range(10)]
    # 9. Medium random coordinates (n = 300, moderate density)
    t9 = _gen_stones(300, 250, 9471)
    # 10. Max-size stress test (n = 1000, coordinates up to 10000)
    t10 = _gen_stones(1000, 10000, 9472)

    return [{"in": {"stones": t}} for t in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
