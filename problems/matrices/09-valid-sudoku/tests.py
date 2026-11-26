def _from_rows(rows):
    return [list(r) for r in rows]


def visible():
    valid = _from_rows([
        "53..7....",
        "6..195...",
        ".98....6.",
        "8...6...3",
        "4..8.3..1",
        "7...2...6",
        ".6....28.",
        "...419..5",
        "....8..79",
    ])
    invalid = _from_rows([
        "83..7....",
        "6..195...",
        ".98....6.",
        "8...6...3",
        "4..8.3..1",
        "7...2...6",
        ".6....28.",
        "...419..5",
        "....8..79",
    ])
    return [
        {"in": {"board": valid}},
        {"in": {"board": invalid}},
    ]


def hidden():
    empty = [["."] * 9 for _ in range(9)]

    solved = _from_rows([
        "534678912",
        "672195348",
        "198342567",
        "859761423",
        "426853791",
        "713924856",
        "961537284",
        "287419635",
        "345286179",
    ])

    row_dup_only = [["."] * 9 for _ in range(9)]
    row_dup_only[4][1] = "6"
    row_dup_only[4][7] = "6"

    col_dup_only = [["."] * 9 for _ in range(9)]
    col_dup_only[1][5] = "3"
    col_dup_only[8][5] = "3"

    box_dup_center = [["."] * 9 for _ in range(9)]
    box_dup_center[3][3] = "7"
    box_dup_center[5][5] = "7"

    box_dup_br = [["."] * 9 for _ in range(9)]
    box_dup_br[6][6] = "9"
    box_dup_br[8][8] = "9"

    # Valid according to rules, though unsolvable (cell (0,8) has no valid digit left)
    valid_unsolvable = _from_rows([
        "12345678.",
        ".........",
        ".........",
        "........9",
        ".........",
        ".........",
        ".........",
        ".........",
        ".........",
    ])

    single = [["."] * 9 for _ in range(9)]
    single[8][8] = "9"

    full_one_dup = [row[:] for row in solved]
    full_one_dup[8][8] = "1"

    # Digits placed across adjacent box boundaries (valid, checks off-by-one box indexing)
    boundary_valid = [["."] * 9 for _ in range(9)]
    boundary_valid[2][2] = "5"
    boundary_valid[3][3] = "5"
    boundary_valid[5][5] = "5"
    boundary_valid[6][6] = "5"
    boundary_valid[2][3] = "4"
    boundary_valid[3][2] = "4"

    return [
        {"in": {"board": empty}},
        {"in": {"board": solved}},
        {"in": {"board": row_dup_only}},
        {"in": {"board": col_dup_only}},
        {"in": {"board": box_dup_center}},
        {"in": {"board": box_dup_br}},
        {"in": {"board": valid_unsolvable}},
        {"in": {"board": single}},
        {"in": {"board": full_one_dup}},
        {"in": {"board": boundary_valid}},
    ]
