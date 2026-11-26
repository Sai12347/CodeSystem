import random


def visible():
    return [
        {"in": {"grid": [[0, 1], [1, 0]]}},
        {"in": {"grid": [[0, 0, 0], [1, 1, 0], [1, 1, 0]]}},
        {"in": {"grid": [[1, 0, 0], [1, 1, 0], [1, 1, 0]]}},
    ]


def hidden():
    tests = []

    # 1. Single cell open
    tests.append({"in": {"grid": [[0]]}})

    # 2. Single cell blocked
    tests.append({"in": {"grid": [[1]]}})

    # 3. Destination cell blocked
    tests.append({"in": {"grid": [[0, 0, 0], [0, 0, 0], [0, 0, 1]]}})

    # 4. Completely disconnected by a horizontal wall
    tests.append({"in": {"grid": [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]}})

    # 5. All-zero 10x10 grid (pure diagonal length 10)
    tests.append({"in": {"grid": [[0] * 10 for _ in range(10)]}})

    # 6. Diagonal-only squeeze: 4-directional movement fails, 8-directional succeeds
    tests.append({"in": {"grid": [
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0],
    ]}})

    # 7. Winding corridor requiring UP and LEFT moves
    tests.append({"in": {"grid": [
        [0, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0],
    ]}})

    # 8. Medium random sparse grid (25x25)
    rng = random.Random(10911)
    g8 = [[1 if rng.random() < 0.28 else 0 for _ in range(25)] for _ in range(25)]
    g8[0][0] = 0
    g8[24][24] = 0
    tests.append({"in": {"grid": g8}})

    # 9. Medium random dense grid (30x30, unreachable)
    rng2 = random.Random(10912)
    g9 = [[1 if rng2.random() < 0.65 else 0 for _ in range(30)] for _ in range(30)]
    g9[0][0] = 0
    g9[29][29] = 0
    tests.append({"in": {"grid": g9}})

    # 10. Stress test: 70x70 grid with random obstacles and guaranteed winding corridor
    rng3 = random.Random(10913)
    n10 = 70
    g10 = [[1 if rng3.random() < 0.32 else 0 for _ in range(n10)] for _ in range(n10)]
    r, c = 0, 0
    g10[0][0] = 0
    while r < n10 - 1 or c < n10 - 1:
        if r < n10 - 1 and (c == n10 - 1 or rng3.random() < 0.5):
            r += 1
        else:
            c += 1
        g10[r][c] = 0
    tests.append({"in": {"grid": g10}})

    return tests
