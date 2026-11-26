def visible():
    return [
        {"in": {"candidates": [2, 3, 6, 7], "target": 7}},
        {"in": {"candidates": [2, 3, 5], "target": 8}},
        {"in": {"candidates": [2], "target": 1}},
    ]


def hidden():
    return [
        {"in": {"candidates": [3], "target": 9}},
        {"in": {"candidates": [4], "target": 10}},
        {"in": {"candidates": [8, 7, 4, 3], "target": 11}},
        {"in": {"candidates": [10, 20, 30], "target": 5}},
        {"in": {"candidates": [40, 20, 15, 25], "target": 40}},
        {"in": {"candidates": [2, 4, 6, 8], "target": 15}},
        {"in": {"candidates": [5, 10, 15, 20, 25, 30, 35, 40], "target": 40}},
        {"in": {"candidates": [2, 3, 5, 7, 11, 13, 17, 19, 23], "target": 14}},
        {"in": {"candidates": list(range(11, 41)), "target": 35}},
        {"in": {"candidates": [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 40], "target": 24}},
    ]
