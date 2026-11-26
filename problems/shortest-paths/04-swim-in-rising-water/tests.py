import random


def _rand_perm_grid(n, seed):
    vals = list(range(n * n))
    random.Random(seed).shuffle(vals)
    return [vals[i * n:(i + 1) * n] for i in range(n)]


def visible():
    return [
        {"in": {"grid": [[0, 2], [1, 3]]}},
        {"in": {"grid": [
            [0, 1, 2, 3, 4],
            [24, 23, 22, 21, 5],
            [12, 13, 14, 15, 16],
            [11, 17, 18, 19, 20],
            [10, 9, 8, 7, 6],
        ]}},
        {"in": {"grid": [[3, 2], [0, 1]]}},
    ]


def hidden():
    tests = []

    # 1. Single cell 1x1
    tests.append({"in": {"grid": [[0]]}})

    # 2. 2x2 where start > end
    tests.append({"in": {"grid": [[1, 0], [3, 2]]}})

    # 3. 3x3 row-major sorted
    tests.append({"in": {"grid": [[0, 1, 2], [3, 4, 5], [6, 7, 8]]}})

    # 4. 3x3 reverse-sorted (start has max elevation)
    tests.append({"in": {"grid": [[8, 7, 6], [5, 4, 3], [2, 1, 0]]}})

    # 5. 5x5 winding path requiring UP and LEFT moves
    snake = [[-1] * 5 for _ in range(5)]
    path = [
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
        (4, 1), (4, 2), (3, 2), (2, 2), (1, 2),
        (0, 2), (0, 3), (0, 4), (1, 4), (2, 4),
        (3, 4), (4, 4),
    ]
    for idx, (r, c) in enumerate(path):
        snake[r][c] = idx
    nxt = len(path)
    for r in range(5):
        for c in range(5):
            if snake[r][c] == -1:
                snake[r][c] = nxt
                nxt += 1
    tests.append({"in": {"grid": snake}})

    # 6. 6x6 inward spiral permutation
    n6 = 6
    spiral = [[0] * n6 for _ in range(n6)]
    top, bot, left, right = 0, n6 - 1, 0, n6 - 1
    val = 0
    while top <= bot and left <= right:
        for c in range(left, right + 1):
            spiral[top][c] = val
            val += 1
        top += 1
        for r in range(top, bot + 1):
            spiral[r][right] = val
            val += 1
        right -= 1
        if top <= bot:
            for c in range(right, left - 1, -1):
                spiral[bot][c] = val
                val += 1
            bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1):
                spiral[r][left] = val
                val += 1
            left += 1
    tests.append({"in": {"grid": spiral}})

    # 7. 8x8 random permutation
    tests.append({"in": {"grid": _rand_perm_grid(8, 7781)}})

    # 8. 20x20 random permutation
    tests.append({"in": {"grid": _rand_perm_grid(20, 7782)}})

    # 9. 35x35 random permutation
    tests.append({"in": {"grid": _rand_perm_grid(35, 7783)}})

    # 10. Stress test: max-size 50x50 random permutation
    tests.append({"in": {"grid": _rand_perm_grid(50, 7784)}})

    return tests
