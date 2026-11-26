def visible():
    return [
        {"in": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 3}},
        {"in": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 13}},
    ]


def hidden():
    # Build a 50x50 strictly increasing matrix with gaps of 2 (values -5000..4998)
    big = [[-5000 + (r * 50 + c) * 2 for c in range(50)] for r in range(50)]
    dup_rows = [
        [-100, -100, -50, -50],
        [-10, 0, 0, 0],
        [5, 5, 5, 5],
        [10, 20, 20, 30],
    ]
    return [
        {"in": {"matrix": [[5]], "target": 5}},
        {"in": {"matrix": [[5]], "target": 4}},
        {"in": {"matrix": [[-10, -3, 0, 4, 9, 15]], "target": 9}},
        {"in": {"matrix": [[-20], [-5], [0], [8], [42]], "target": -5}},
        {"in": {"matrix": [[1, 3, 5], [10, 12, 14], [20, 22, 24]], "target": 1}},
        {"in": {"matrix": [[1, 3, 5], [10, 12, 14], [20, 22, 24]], "target": 24}},
        {"in": {"matrix": [[1, 3, 5], [10, 12, 14], [20, 22, 24]], "target": -10000}},
        {"in": {"matrix": [[1, 3, 5], [10, 12, 14], [20, 22, 24]], "target": 10000}},
        {"in": {"matrix": dup_rows, "target": 0}},
        {"in": {"matrix": dup_rows, "target": 6}},
        {"in": {"matrix": big, "target": big[37][49]}},
        {"in": {"matrix": big, "target": big[24][49] + 1}},
    ]
