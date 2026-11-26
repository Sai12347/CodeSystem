import random


def visible():
    return [
        {"in": {"grid": ["@.a..", "###.#", "b.A.B"]}},
        {"in": {"grid": ["@..aA", "..B#.", "....b"]}},
        {"in": {"grid": ["@Aa"]}},
    ]


def hidden():
    tests = []

    # 1. Single row, 1 key immediately reachable (lock behind it)
    tests.append({"in": {"grid": ["@.aA"]}})

    # 2. Single column, 1 key reachable while lock is blocked behind wall
    tests.append({"in": {"grid": ["@", ".", "a", "#", "A"]}})

    # 3. Must backtrack past '@' after picking up 'a' to unlock 'A' and reach 'b'
    tests.append({"in": {"grid": ["b.A.@.a.B"]}})

    # 4. Deadlock cycle: 'a' behind 'B' and 'b' behind 'A'
    tests.append({"in": {"grid": [
        "@.#",
        "A#B",
        "b#a",
    ]}})

    # 5. 3 keys where greedy nearest-key order is suboptimal
    tests.append({"in": {"grid": [
        "c..#..B",
        "###.###",
        "b..@..a",
        "###.###",
        "A..#..C",
    ]}})

    # 6. 4 keys sequential unlock chain a -> A -> b -> B -> c -> C -> d
    tests.append({"in": {"grid": [
        "@.a#b.B",
        "##A#.#.",
        "D#.#.#c",
        ".#dC.#.",
    ]}})

    # 7. 5 keys in a 10x10 room with walls and locks
    tests.append({"in": {"grid": [
        "@...#....a",
        ".##.#.##..",
        ".#..A....#",
        ".#.####.##",
        "b..#..c..#",
        "##.#.##.##",
        "B..#..C..D",
        ".####.###.",
        "d...E...e#",
        "..........",
    ]}})

    # 8. 6 keys in a 10x10 maze with locks guarding corridors
    tests.append({"in": {"grid": [
        "@.a.#.b.A.",
        "###.#.###.",
        "B.c.#.C.d.",
        ".##.#####.",
        ".#D...E.e.",
        ".#.######.",
        ".#.f#F....",
        ".#..#.##..",
        "....#.....",
        "..........",
    ]}})

    # 9. Impossible with 6 keys (key 'f' completely walled off)
    tests.append({"in": {"grid": [
        "@.a.b.c",
        ".A.B.C.",
        "d.e.D.E",
        "#####F#",
        "....#f#",
    ]}})

    # 10. Stress test: 30x30 grid with 6 keys (a..f) and 6 locks (A..F)
    rng = random.Random(8641)
    m, n = 30, 30
    board = [["." for _ in range(n)] for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if rng.random() < 0.22:
                board[r][c] = "#"
    specials = [
        ("@", 0, 0),
        ("a", 2, 27), ("A", 5, 14),
        ("b", 12, 3), ("B", 15, 15),
        ("c", 20, 26), ("C", 22, 10),
        ("d", 28, 2), ("D", 10, 20),
        ("e", 14, 28), ("E", 25, 20),
        ("f", 29, 29), ("F", 18, 5),
    ]
    # Clear a spanning backbone so specials are reachable
    for r in range(m):
        board[r][0] = "."
        board[r][29] = "."
    for c in range(n):
        board[0][c] = "."
        board[14][c] = "."
        board[29][c] = "."
    for ch, r, c in specials:
        board[r][c] = ch
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "#":
                board[nr][nc] = "."
    tests.append({"in": {"grid": ["".join(row) for row in board]}})

    return tests
