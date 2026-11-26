import random


def _from_rows(rows):
    return [list(r) for r in rows]


def visible():
    b1 = _from_rows([
        "XXXX",
        "XOOX",
        "XXOX",
        "XOXX",
    ])
    b2 = _from_rows(["X"])
    b3 = _from_rows([
        "XXX",
        "XOX",
        "XXX",
    ])
    return [
        {"in": {"board": b1}},
        {"in": {"board": b2}},
        {"in": {"board": b3}},
    ]


def hidden():
    tests = []

    # 1. Single cell 'O' (on border, stays 'O')
    tests.append({"in": {"board": [["O"]]}})

    # 2. 2x2 all 'O' (every cell is on border)
    tests.append({"in": {"board": [["O", "O"], ["O", "O"]]}})

    # 3. Single row 1x8 mixed
    tests.append({"in": {"board": [list("XOOXXOXO")]}})

    # 4. Single column 8x1 mixed
    tests.append({"in": {"board": [[ch] for ch in "OXOOXXOX"]}})

    # 5. All 'X' 5x5
    tests.append({"in": {"board": [["X"] * 5 for _ in range(5)]}})

    # 6. All 'O' 5x5
    tests.append({"in": {"board": [["O"] * 5 for _ in range(5)]}})

    # 7. Diagonal border contact does NOT save interior 'O'
    diag = _from_rows([
        "OXXXX",
        "XOXXX",
        "XXOXX",
        "XXXOX",
        "XXXXO",
    ])
    tests.append({"in": {"board": diag}})

    # 8. Winding safe corridor alongside an enclosed interior pocket
    corridor = _from_rows([
        "XXXXXXX",
        "XOOOOOX",
        "XOXXXOX",
        "XOXOXOX",
        "XOXXXOX",
        "XOOXOOX",
        "XXOXXXX",
    ])
    tests.append({"in": {"board": corridor}})

    # 9. Concentric rings of 'O' and 'X' (9x9): outer 'O' ring safe, inner 'O' ring captured
    n = 9
    rings = [["X"] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            layer = min(r, c, n - 1 - r, n - 1 - c)
            if layer % 2 == 0:
                rings[r][c] = "O"
    tests.append({"in": {"board": rings}})

    # 10. Medium random board (40x40)
    rng1 = random.Random(1301)
    g10 = [["O" if rng1.random() < 0.55 else "X" for _ in range(40)] for _ in range(40)]
    tests.append({"in": {"board": g10}})

    # 11. Larger random board (55x55, ~12KB JSON)
    rng2 = random.Random(1302)
    g11 = [["O" if rng2.random() < 0.48 else "X" for _ in range(55)] for _ in range(55)]
    tests.append({"in": {"board": g11}})

    return tests
