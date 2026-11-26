import random


def visible():
    return [
        {"in": {"intervals": [[1, 3], [6, 9]], "newInterval": [2, 5]}},
        {"in": {"intervals": [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], "newInterval": [4, 8]}},
        {"in": {"intervals": [], "newInterval": [5, 7]}},
    ]


def hidden():
    rng = random.Random(57)
    # Build sorted non-overlapping intervals
    stress1 = []
    cur = 0
    for _ in range(1500):
        cur += rng.randint(1, 30)
        end = cur + rng.randint(0, 25)
        if end > 100000:
            break
        stress1.append([cur, end])
        cur = end

    stress2 = [[i * 5, i * 5 + 3] for i in range(2000)]

    return [
        {"in": {"intervals": [[3, 5], [8, 10]], "newInterval": [0, 1]}},
        {"in": {"intervals": [[1, 2], [4, 6]], "newInterval": [8, 10]}},
        {"in": {"intervals": [[1, 10]], "newInterval": [3, 5]}},
        {"in": {"intervals": [[2, 3], [5, 6], [8, 9]], "newInterval": [0, 12]}},
        {"in": {"intervals": [[1, 2], [5, 6]], "newInterval": [2, 5]}},
        {"in": {"intervals": [[0, 0], [2, 2], [4, 4]], "newInterval": [1, 1]}},
        {"in": {"intervals": [[0, 0], [2, 2]], "newInterval": [0, 0]}},
        {"in": {"intervals": [[1, 5]], "newInterval": [6, 8]}},
        {"in": {"intervals": [[0, 50000], [50002, 100000]], "newInterval": [50000, 50002]}},
        {"in": {"intervals": stress1, "newInterval": [10000, 25000]}},
        {"in": {"intervals": stress2, "newInterval": [2500, 7500]}},
    ]
