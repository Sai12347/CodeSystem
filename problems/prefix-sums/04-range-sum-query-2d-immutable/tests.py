import random


def visible():
    mat1 = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ]
    mat2 = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    return [
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[mat1], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[mat2], [0, 0, 0, 0], [0, 0, 0, 2], [0, 1, 1, 1], [0, 0, 1, 2]]
        }},
    ]


def hidden():
    rng = random.Random(304)
    big_mat = [[rng.randint(-10000, 10000) for _ in range(40)] for _ in range(40)]
    ops_big = ["NumMatrix"]
    args_big = [[big_mat]]
    for _ in range(250):
        r1 = rng.randint(0, 39)
        r2 = rng.randint(r1, 39)
        c1 = rng.randint(0, 39)
        c2 = rng.randint(c1, 39)
        ops_big.append("sumRegion")
        args_big.append([r1, c1, r2, c2])

    rect_mat = [[(r * 17 - c * 13) % 21 - 10 for c in range(30)] for r in range(15)]
    ops_rect = ["NumMatrix", "sumRegion", "sumRegion", "sumRegion", "sumRegion", "sumRegion"]
    args_rect = [[rect_mat], [0, 0, 14, 29], [0, 0, 0, 29], [0, 29, 14, 29], [5, 10, 12, 25], [14, 29, 14, 29]]

    const_mat = [[10000] * 25 for _ in range(25)]
    ops_const = ["NumMatrix", "sumRegion", "sumRegion"]
    args_const = [[const_mat], [0, 0, 24, 24], [5, 5, 19, 19]]

    return [
        {"in": {
            "ops": ["NumMatrix", "sumRegion"],
            "args": [[[[-7]]], [0, 0, 0, 0]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[[[1, -2, 3, -4, 5]]], [0, 0, 0, 4], [0, 1, 0, 3], [0, 4, 0, 4]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[[[1], [-2], [3], [-4], [5]]], [0, 0, 4, 0], [1, 0, 3, 0], [2, 0, 2, 0]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [0, 0, 2, 2], [1, 1, 2, 2], [0, 2, 0, 2]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[[[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]]], [0, 0, 2, 2], [1, 1, 2, 2], [0, 0, 1, 1], [2, 0, 2, 2]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[[[1, -1, 1, -1], [-1, 1, -1, 1], [1, -1, 1, -1], [-1, 1, -1, 1]]], [0, 0, 3, 3], [0, 0, 2, 2], [1, 1, 3, 3], [0, 1, 2, 3]]
        }},
        {"in": {
            "ops": ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"],
            "args": [[[[-10000, 10000], [10000, -10000]]], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1]]
        }},
        {"in": {"ops": ops_rect, "args": args_rect}},
        {"in": {"ops": ops_const, "args": args_const}},
        {"in": {"ops": ops_big, "args": args_big}},
    ]
