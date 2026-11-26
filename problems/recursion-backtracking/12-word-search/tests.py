def visible():
    b = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    return [
        {"in": {"board": b, "word": "ABCCED"}},
        {"in": {"board": b, "word": "SEE"}},
        {"in": {"board": b, "word": "ABCB"}},
    ]


def hidden():
    # Adversarial 6x6 board with isolated 'B' surrounded by 'C's so frequency check passes
    iso_board = [["A"] * 6 for _ in range(6)]
    iso_board[0][0] = "B"
    iso_board[0][1] = "C"
    iso_board[1][0] = "C"

    # Adversarial 6x6 board with 'B' reachable at bottom-right
    reach_board = [["A"] * 6 for _ in range(6)]
    reach_board[5][5] = "B"

    return [
        # 1x1 exact match
        {"in": {"board": [["a"]], "word": "a"}},
        # 1x1 case-sensitivity mismatch
        {"in": {"board": [["a"]], "word": "A"}},
        # Single row reverse traversal
        {"in": {"board": [["a", "b", "c", "d", "e", "f"]], "word": "fedcba"}},
        # Single column word longer than total cells
        {"in": {"board": [["A"], ["B"], ["C"], ["D"]], "word": "ABCDE"}},
        # Diagonal-only path (must return False)
        {"in": {"board": [["A", "X", "X"], ["X", "B", "X"], ["X", "X", "C"]], "word": "ABC"}},
        # Self-intersection / revisit trap (T-shape needs revisiting center 'B')
        {"in": {"board": [["X", "A", "X"], ["C", "B", "D"], ["X", "E", "X"]], "word": "ABCBDE"}},
        # Full 3x4 snake path using all 12 cells
        {"in": {"board": [
            ["A", "B", "C", "D"],
            ["H", "G", "F", "E"],
            ["I", "J", "K", "L"],
        ], "word": "ABCDEFGHIJKL"}},
        # Multiple dead-end branches requiring clean visited restoration
        {"in": {"board": [
            ["C", "A", "A"],
            ["A", "A", "A"],
            ["B", "C", "D"],
        ], "word": "AAB"}},
        # Mixed case valid winding path
        {"in": {"board": [
            ["a", "A", "b", "B"],
            ["c", "C", "d", "D"],
            ["e", "E", "f", "F"],
        ], "word": "aACdDFfEec"}},
        # Adversarial stress test (True): 14 'A's + 'B' at far corner
        {"in": {"board": reach_board, "word": "AAAAAAAAAAAAAAB"}},
        # Adversarial stress test (False): 'B' exists but is blocked by 'C's
        {"in": {"board": iso_board, "word": "AAAAAAAAAAAAAAB"}},
    ]
