import random


def _gen_sorted_matrix(n, seed, base=-50, max_step=7):
    rng = random.Random(seed)
    mat = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if r == 0 and c == 0:
                mat[r][c] = base
            elif r == 0:
                mat[r][c] = mat[r][c - 1] + rng.randint(0, max_step)
            elif c == 0:
                mat[r][c] = mat[r - 1][c] + rng.randint(0, max_step)
            else:
                mat[r][c] = max(mat[r - 1][c], mat[r][c - 1]) + rng.randint(0, max_step)
    return mat


def visible():
    return [
        {"in": {"matrix": [[1, 5, 9], [10, 11, 13], [12, 13, 15]], "k": 8}},
        {"in": {"matrix": [[-5]], "k": 1}},
        {"in": {"matrix": [[1, 2], [3, 4]], "k": 3}},
    ]


def hidden():
    mat_large = _gen_sorted_matrix(50, seed=37801, base=-1000, max_step=9)
    mat_dups = _gen_sorted_matrix(40, seed=37802, base=-5, max_step=1)

    return [
        {"in": {"matrix": [[1, 2], [1, 3]], "k": 2}},
        {"in": {"matrix": [[7, 7, 7], [7, 7, 7], [7, 7, 7]], "k": 5}},
        {"in": {"matrix": [[-1000000000, -500000000], [0, 1000000000]], "k": 1}},
        {"in": {"matrix": [[-1000000000, -500000000], [0, 1000000000]], "k": 4}},
        {"in": {"matrix": [[1, 3, 5, 7], [2, 4, 6, 8], [3, 5, 7, 9], [4, 6, 8, 10]], "k": 9}},
        {"in": {"matrix": [[-20, -15, -10], [-18, -12, -5], [-16, -8, -1]], "k": 6}},
        {"in": {"matrix": [[1, 100, 200], [2, 101, 201], [3, 102, 202]], "k": 3}},
        {"in": {"matrix": [[1, 2, 3], [100, 101, 102], [200, 201, 202]], "k": 4}},
        {"in": {"matrix": mat_large, "k": 1777}},
        {"in": {"matrix": mat_dups, "k": 900}},
    ]
