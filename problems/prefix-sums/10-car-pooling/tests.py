import random


def _peak_occupancy(trips):
    diff = [0] * 1001
    for p, start, end in trips:
        diff[start] += p
        diff[end] -= p
    cur = 0
    best = 0
    for d in diff:
        cur += d
        if cur > best:
            best = cur
    return best


def visible():
    return [
        {"in": {"trips": [[2, 1, 5], [3, 3, 7]], "capacity": 4}},
        {"in": {"trips": [[2, 1, 5], [3, 3, 7]], "capacity": 5}},
        {"in": {"trips": [[3, 2, 7], [3, 7, 9], [8, 3, 9]], "capacity": 11}},
    ]


def hidden():
    rng1 = random.Random(10941)
    stress1 = []
    for _ in range(1000):
        a = rng1.randint(0, 999)
        b = rng1.randint(a + 1, 1000)
        p = rng1.randint(1, 100)
        stress1.append([p, a, b])
    peak1 = _peak_occupancy(stress1)

    rng2 = random.Random(10942)
    stress2 = []
    for _ in range(1000):
        a = rng2.randint(0, 999)
        b = rng2.randint(a + 1, 1000)
        p = rng2.randint(1, 100)
        stress2.append([p, a, b])
    peak2 = _peak_occupancy(stress2)

    return [
        {"in": {"trips": [[5, 0, 1]], "capacity": 5}},
        {"in": {"trips": [[6, 0, 1]], "capacity": 5}},
        {"in": {"trips": [[4, 0, 5], [4, 5, 10], [4, 10, 15]], "capacity": 4}},
        {"in": {"trips": [[3, 5, 8], [2, 1, 6], [4, 5, 8], [1, 0, 10]], "capacity": 10}},
        {"in": {"trips": [[3, 5, 8], [2, 1, 6], [4, 5, 8], [1, 0, 10]], "capacity": 9}},
        {"in": {"trips": [[100, 0, 1000], [100, 0, 1000]], "capacity": 200}},
        {"in": {"trips": [[100, 0, 1000], [100, 0, 1000], [1, 500, 501]], "capacity": 200}},
        {"in": {"trips": [[10, 100, 200], [20, 200, 300], [30, 150, 250], [15, 250, 350]], "capacity": 50}},
        {"in": {"trips": [[5, 2, 4], [5, 2, 4], [5, 2, 4], [5, 4, 6], [5, 4, 6], [5, 4, 6]], "capacity": 15}},
        {"in": {"trips": stress1, "capacity": peak1}},
        {"in": {"trips": stress2, "capacity": peak2 - 1}},
    ]
