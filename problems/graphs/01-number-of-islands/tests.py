import random


def _from_rows(rows):
    return [list(r) for r in rows]


def visible():
    g1 = _from_rows([
        "11110",
        "11010",
        "11000",
        "00000",
    ])
    g2 = _from_rows([
        "11000",
        "11000",
        "00100",
        "00011",
    ])
    g3 = _from_rows([
        "101",
        "010",
        "101",
    ])
    return [
        {"in": {"grid": g1}},
        {"in": {"grid": g2}},
        {"in": {"grid": g3}},
    ]


def hidden():
    tests = []

    # 1. Single cell water
    tests.append({"in": {"grid": [["0"]]}})

    # 2. Single cell land
    tests.append({"in": {"grid": [["1"]]}})

    # 3. All water 5x5
    tests.append({"in": {"grid": [["0"] * 5 for _ in range(5)]}})

    # 4. All land 5x5
    tests.append({"in": {"grid": [["1"] * 5 for _ in range(5)]}})

    # 5. Single row with alternating blocks
    tests.append({"in": {"grid": [list("101100101110")]}})

    # 6. Single column with alternating blocks
    tests.append({"in": {"grid": [[ch] for ch in "01101001101"]}})

    # 7. Concentric rings (island inside water inside island)
    n = 11
    rings = [["0"] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            layer = min(r, c, n - 1 - r, n - 1 - c)
            if layer % 2 == 0:
                rings[r][c] = "1"
    tests.append({"in": {"grid": rings}})

    # 8. Long snake / winding single island (25x25) to stress recursion depth
    s = 25
    snake = [["0"] * s for _ in range(s)]
    for r in range(0, s, 2):
        for c in range(s):
            snake[r][c] = "1"
        if r + 1 < s:
            if (r // 2) % 2 == 0:
                snake[r + 1][s - 1] = "1"
            else:
                snake[r + 1][0] = "1"
    tests.append({"in": {"grid": snake}})

    # 9. Medium random dense grid (35x35)
    rng = random.Random(2001)
    g9 = [["1" if rng.random() < 0.52 else "0" for _ in range(35)] for _ in range(35)]
    tests.append({"in": {"grid": g9}})

    # 10. Larger random grid (55x55, ~12KB JSON)
    rng2 = random.Random(2002)
    g10 = [["1" if rng2.random() < 0.45 else "0" for _ in range(55)] for _ in range(55)]
    tests.append({"in": {"grid": g10}})

    return tests
