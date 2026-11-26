def visible():
    base = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    return [
        {"in": {"matrix": base, "target": 5}},
        {"in": {"matrix": base, "target": 20}},
    ]


def hidden():
    # 50x50 matrix where every row and col is strictly increasing with overlapping ranges
    big = [[(r * 3 + c * 2) * 2 - 200 for c in range(50)] for r in range(50)]
    dups = [
        [-1000000000, -10, -10, 0, 5],
        [-10, -10, 0, 5, 5],
        [0, 0, 5, 5, 100],
        [5, 5, 5, 100, 1000000000],
    ]
    overlap = [
        [1, 10, 20, 30],
        [2, 11, 21, 31],
        [3, 12, 22, 32],
    ]
    return [
        {"in": {"matrix": [[7]], "target": 7}},
        {"in": {"matrix": [[7]], "target": -7}},
        {"in": {"matrix": [[-5, -1, 0, 4, 9, 12]], "target": 12}},
        {"in": {"matrix": [[-5], [-1], [0], [4], [9], [12]], "target": 3}},
        {"in": {"matrix": overlap, "target": 30}},
        {"in": {"matrix": overlap, "target": 3}},
        {"in": {"matrix": overlap, "target": 0}},
        {"in": {"matrix": dups, "target": -1000000000}},
        {"in": {"matrix": dups, "target": 1000000000}},
        {"in": {"matrix": dups, "target": 4}},
        {"in": {"matrix": big, "target": big[49][0]}},
        {"in": {"matrix": big, "target": big[25][25] + 1}},
    ]
