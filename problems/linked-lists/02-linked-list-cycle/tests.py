def visible():
    return [
        {"in": {"head": [3, 2, 0, -4], "pos": 1}},
        {"in": {"head": [1, 2], "pos": -1}},
        {"in": {"head": [1], "pos": 0}},
    ]


def hidden():
    return [
        {"in": {"head": [], "pos": -1}},
        {"in": {"head": [1], "pos": -1}},
        {"in": {"head": [1, 2], "pos": 0}},
        {"in": {"head": [1, 2], "pos": 1}},
        {"in": {"head": [1, 1, 1, 1], "pos": -1}},
        {"in": {"head": [1, 1, 1, 1], "pos": 2}},
        {"in": {"head": list(range(100)), "pos": 0}},
        {"in": {"head": list(range(100)), "pos": 99}},
        {"in": {"head": list(range(2000)), "pos": -1}},
        {"in": {"head": list(range(2000)), "pos": 1234}},
    ]
