import random


def visible():
    return [
        {"in": {"list1": [1, 2, 4], "list2": [1, 3, 4]}},
        {"in": {"list1": [], "list2": []}},
        {"in": {"list1": [], "list2": [0]}},
    ]


def hidden():
    rng = random.Random(21)
    a = sorted(rng.randint(-100000, 100000) for _ in range(1500))
    b = sorted(rng.randint(-100000, 100000) for _ in range(1500))
    return [
        {"in": {"list1": [5], "list2": []}},
        {"in": {"list1": [1], "list2": [1]}},
        {"in": {"list1": [-10, -5, 0], "list2": [-20, -5, 5, 10]}},
        {"in": {"list1": [1, 2, 3], "list2": [4, 5, 6]}},
        {"in": {"list1": [10, 20, 30], "list2": [-5, -2, 0]}},
        {"in": {"list1": [3, 3, 3, 3], "list2": [3, 3, 3]}},
        {"in": {"list1": [-100000, 0, 100000], "list2": [-100000, -1, 1, 100000]}},
        {"in": {"list1": [1, 500, 1000], "list2": list(range(0, 100))}},
        {"in": {"list1": a, "list2": b}},
        {"in": {"list1": list(range(0, 4000, 2)), "list2": list(range(1, 4000, 2))}},
    ]
