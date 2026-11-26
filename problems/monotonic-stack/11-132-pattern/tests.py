import random


def visible():
    return [
        {"in": {"nums": [1, 2, 3, 4]}},
        {"in": {"nums": [3, 1, 4, 2]}},
        {"in": {"nums": [-1, 3, 2, 0]}},
    ]


def hidden():
    v_shape_false = list(range(1000, 0, -1)) + list(range(1, 1001))
    buried_true = list(range(1000, 0, -1)) + [5, 100, 50] + list(range(101, 1001))
    return [
        {"in": {"nums": [5]}},
        {"in": {"nums": [1, 3]}},
        {"in": {"nums": [10, 9, 8, 7, 6, 5]}},
        {"in": {"nums": [2, 2, 2, 2, 2]}},
        {"in": {"nums": [1, 3, 1, 3, 1]}},
        {"in": {"nums": [3, 5, 0, 3, 4]}},
        {"in": {"nums": [-10**9, 10**9, 0]}},
        {"in": {"nums": [-10**9, 10**9, -10**9]}},
        {"in": {"nums": [1, 0, 1, -4, -3]}},
        {"in": {"nums": [1, 4, 0, -1, -2, -3, -1, -2]}},
        {"in": {"nums": v_shape_false}},
        {"in": {"nums": buried_true}},
    ]
