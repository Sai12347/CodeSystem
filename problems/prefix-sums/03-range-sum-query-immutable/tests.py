import random


def visible():
    return [
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange"],
            "args": [[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange"],
            "args": [[[10, 20, 30, 40]], [0, 0], [3, 3], [0, 3]]
        }},
    ]


def hidden():
    rng = random.Random(303)
    big_nums = [rng.randint(-10**5, 10**5) for _ in range(2000)]
    ops_big = ["NumArray"]
    args_big = [[big_nums]]
    for _ in range(400):
        a = rng.randint(0, 1999)
        b = rng.randint(a, 1999)
        ops_big.append("sumRange")
        args_big.append([a, b])

    max_nums = [10**5] * 2000
    ops_max = ["NumArray", "sumRange", "sumRange", "sumRange"]
    args_max = [[max_nums], [0, 1999], [500, 1499], [1999, 1999]]

    min_nums = [-10**5] * 2000
    ops_min = ["NumArray", "sumRange", "sumRange"]
    args_min = [[min_nums], [0, 1999], [100, 200]]

    return [
        {"in": {
            "ops": ["NumArray", "sumRange"],
            "args": [[[42]], [0, 0]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange"],
            "args": [[[0, 0, 0, 0, 0]], [0, 4], [1, 3], [2, 2]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange", "sumRange"],
            "args": [[[-1, -2, -3, -4, -5]], [0, 0], [0, 4], [2, 4], [1, 2]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange", "sumRange"],
            "args": [[[5, -5, 5, -5, 5, -5]], [0, 5], [0, 4], [1, 4], [2, 3]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange", "sumRange", "sumRange"],
            "args": [[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], [0, 9], [0, 4], [5, 9], [3, 7], [4, 4]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange"],
            "args": [[[-100000, 100000]], [0, 1], [1, 1]]
        }},
        {"in": {
            "ops": ["NumArray", "sumRange", "sumRange", "sumRange"],
            "args": [[[7, 7, 7, 7, 7, 7]], [0, 5], [1, 4], [2, 2]]
        }},
        {"in": {"ops": ops_max, "args": args_max}},
        {"in": {"ops": ops_min, "args": args_min}},
        {"in": {"ops": ops_big, "args": args_big}},
    ]
