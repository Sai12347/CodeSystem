import random


def visible():
    return [
        {"in": {"matrix": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]}},
        {"in": {"matrix": [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]}},
    ]


def hidden():
    rng = random.Random(7303)
    # Sparse 40x50 matrix with ~3% zeroes and extreme int32 values
    stress = []
    for r in range(40):
        row = []
        for c in range(50):
            if rng.random() < 0.015:
                row.append(0)
            else:
                v = rng.randint(-1000, 1000)
                row.append(v if v != 0 else 1)
        stress.append(row)
    stress[0][49] = 2147483647
    stress[39][0] = -2147483648

    diag = [[0 if r == c else r * 5 + c + 1 for c in range(5)] for r in range(5)]
    return [
        {"in": {"matrix": [[0]]}},
        {"in": {"matrix": [[7]]}},
        {"in": {"matrix": [[1, 2, 0, 4, 5]]}},
        {"in": {"matrix": [[1], [0], [3], [4], [5]]}},
        {"in": {"matrix": [[1, 0, 3], [4, 5, 6], [7, 8, 9]]}},
        {"in": {"matrix": [[1, 2, 3], [0, 5, 6], [7, 8, 9]]}},
        {"in": {"matrix": [[0, 2, 3], [4, 5, 6], [7, 8, 9]]}},
        {"in": {"matrix": [[-2147483648, 2147483647], [-1, 1]]}},
        {"in": {"matrix": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]}},
        {"in": {"matrix": diag}},
        {"in": {"matrix": stress}},
    ]
