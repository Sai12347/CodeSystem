import random


def visible():
    return [
        {"in": {"matrix": [
            ["1", "0", "1", "0", "0"],
            ["1", "0", "1", "1", "1"],
            ["1", "1", "1", "1", "1"],
            ["1", "0", "0", "1", "0"],
        ]}},
        {"in": {"matrix": [["0"]]}},
        {"in": {"matrix": [["1"]]}},
    ]


def hidden():
    rng = random.Random(85)
    checker = [["1" if (r + c) % 2 == 0 else "0" for c in range(6)] for r in range(6)]
    diag_zero = [["0" if r == c else "1" for c in range(8)] for r in range(8)]
    dense_rand = [["1" if rng.random() < 0.78 else "0" for _ in range(35)] for _ in range(35)]
    mostly_ones = [["0" if rng.random() < 0.04 else "1" for _ in range(45)] for _ in range(45)]
    return [
        {"in": {"matrix": [["0"] * 4 for _ in range(4)]}},
        {"in": {"matrix": [["1"] * 6 for _ in range(5)]}},
        {"in": {"matrix": [["1", "0", "1", "1", "1", "0", "1"]]}},
        {"in": {"matrix": [["1"], ["1"], ["0"], ["1"], ["1"], ["1"]]}},
        {"in": {"matrix": checker}},
        {"in": {"matrix": diag_zero}},
        {"in": {"matrix": [
            ["1", "1", "1", "1", "1", "1", "1", "1"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "1", "1", "1", "0", "0", "0", "0"],
            ["0", "1", "1", "1", "0", "0", "0", "0"],
            ["0", "1", "1", "1", "0", "0", "0", "0"],
        ]}},
        {"in": {"matrix": [
            ["0", "1", "1", "0", "1"],
            ["1", "1", "0", "1", "0"],
            ["0", "1", "1", "1", "0"],
            ["1", "1", "1", "1", "0"],
            ["1", "1", "1", "1", "1"],
            ["0", "0", "0", "0", "0"],
        ]}},
        {"in": {"matrix": dense_rand}},
        {"in": {"matrix": mostly_ones}},
    ]
