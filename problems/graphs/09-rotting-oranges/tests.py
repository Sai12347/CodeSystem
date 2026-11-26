import random


def visible():
    return [
        {"in": {"grid": [[2, 1, 1], [1, 1, 0], [0, 1, 1]]}},
        {"in": {"grid": [[2, 1, 1], [0, 1, 1], [1, 0, 1]]}},
        {"in": {"grid": [[0, 2]]}},
    ]


def hidden():
    tests = []

    # 1. 1x1 empty cell -> 0
    tests.append({"in": {"grid": [[0]]}})

    # 2. 1x1 fresh orange -> -1
    tests.append({"in": {"grid": [[1]]}})

    # 3. 1x1 rotten orange -> 0
    tests.append({"in": {"grid": [[2]]}})

    # 4. All fresh oranges, no rotten sources -> -1
    tests.append({"in": {"grid": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]}})

    # 5. All rotten oranges -> 0
    tests.append({"in": {"grid": [[2, 2, 2], [2, 2, 2]]}})

    # 6. Diagonal adjacency does not spread rot -> -1
    tests.append({"in": {"grid": [[2, 0, 1], [0, 1, 0], [1, 0, 2]]}})

    # 7. Multi-source simultaneous spread along a 1x15 row -> 7
    tests.append({"in": {"grid": [[2] + [1] * 13 + [2]]}})

    # 8. Single column 12x1 with empty wall isolating one fresh orange -> -1
    col = [[2], [1], [1], [1], [1], [0], [1], [1], [1], [1], [1], [1]]
    tests.append({"in": {"grid": col}})

    # 9. Snake/zig-zag corridor (15x15) forcing long single-source traversal
    n9 = 15
    snake = [[0] * n9 for _ in range(n9)]
    for r in range(0, n9, 2):
        for c in range(n9):
            snake[r][c] = 1
        if r + 1 < n9:
            turn_col = n9 - 1 if (r // 2) % 2 == 0 else 0
            snake[r + 1][turn_col] = 1
    snake[0][0] = 2
    tests.append({"in": {"grid": snake}})

    # 10. Large stress test: 60x60 grid with multiple rotten sources and deterministic obstacles (all reachable)
    rng = random.Random(9940)
    rows, cols = 60, 60
    grid10 = [[1] * cols for _ in range(rows)]
    # Place sparse non-isolating obstacles (checkerboard-safe walls with gaps)
    for r in range(2, rows - 2, 4):
        gap = rng.randint(1, cols - 2)
        for c in range(1, cols - 1):
            if c != gap and rng.random() < 0.7:
                grid10[r][c] = 0
    # Place rotten sources in all 4 corners and center
    for r, c in ((0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1), (rows // 2, cols // 2)):
        grid10[r][c] = 2
    tests.append({"in": {"grid": grid10}})

    return tests
