import random


def visible():
    g1 = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]
    g2 = [[0, 0, 0, 0, 0, 0, 0, 0]]
    g3 = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ]
    return [
        {"in": {"grid": g1}},
        {"in": {"grid": g2}},
        {"in": {"grid": g3}},
    ]


def hidden():
    tests = []

    # 1. Single cell water
    tests.append({"in": {"grid": [[0]]}})

    # 2. Single cell land
    tests.append({"in": {"grid": [[1]]}})

    # 3. All ones 10x10
    tests.append({"in": {"grid": [[1] * 10 for _ in range(10)]}})

    # 4. All zeros 8x8
    tests.append({"in": {"grid": [[0] * 8 for _ in range(8)]}})

    # 5. Single row 1x50 with varying runs
    row = [0] * 50
    for i in range(2, 7):
        row[i] = 1
    for i in range(15, 29):
        row[i] = 1
    for i in range(40, 49):
        row[i] = 1
    tests.append({"in": {"grid": [row]}})

    # 6. Single column 50x1
    col = [[1 if (5 <= i < 12 or 20 <= i < 37 or 42 <= i < 48) else 0] for i in range(50)]
    tests.append({"in": {"grid": col}})

    # 7. U-shaped island vs equal blocks
    u_grid = [
        [1, 1, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0],
    ]
    tests.append({"in": {"grid": u_grid}})

    # 8. Long winding snake on 25x25
    s = 25
    snake = [[0] * s for _ in range(s)]
    for r in range(0, s, 2):
        for c in range(s):
            snake[r][c] = 1
        if r + 1 < s:
            if (r // 2) % 2 == 0:
                snake[r + 1][s - 1] = 1
            else:
                snake[r + 1][0] = 1
    tests.append({"in": {"grid": snake}})

    # 9. Max-constraint 50x50 medium-density random grid
    rng1 = random.Random(6951)
    g9 = [[1 if rng1.random() < 0.45 else 0 for _ in range(50)] for _ in range(50)]
    tests.append({"in": {"grid": g9}})

    # 10. Max-constraint 50x50 higher-density random grid
    rng2 = random.Random(6952)
    g10 = [[1 if rng2.random() < 0.58 else 0 for _ in range(50)] for _ in range(50)]
    tests.append({"in": {"grid": g10}})

    return tests
