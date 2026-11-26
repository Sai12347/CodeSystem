import random


def _make_mountain(n: int, peak: int, seed: int):
    rng = random.Random(seed)
    left = [0] * (peak + 1)
    cur = rng.randint(0, 10)
    for i in range(peak + 1):
        cur += rng.randint(1, 5)
        left[i] = cur
    peak_val = left[-1]
    right = []
    cur = peak_val
    for _ in range(n - peak - 1):
        cur -= rng.randint(1, 5)
        right.append(cur)
    # Shift up if right tail went negative
    min_val = min(left[0], right[-1])
    if min_val < 0:
        shift = -min_val
        left = [v + shift for v in left]
        right = [v + shift for v in right]
    return left + right


def visible():
    return [
        {"in": {"mountainArr": [1, 2, 3, 4, 5, 3, 1], "target": 3}},
        {"in": {"mountainArr": [0, 1, 2, 4, 2, 1], "target": 3}},
        {"in": {"mountainArr": [1, 5, 2], "target": 2}},
    ]


def hidden():
    m1 = _make_mountain(4000, 2900, 1095)
    t1 = m1[3850]

    m2 = _make_mountain(5000, 1200, 109502)
    t2 = m2[1200] + 1  # strictly above peak -> absent, forces searching peak + both sides

    return [
        {"in": {"mountainArr": [1, 5, 2], "target": 1}},
        {"in": {"mountainArr": [1, 5, 2], "target": 5}},
        {"in": {"mountainArr": [1, 5, 2], "target": 0}},
        {"in": {"mountainArr": [10, 20, 30, 25, 15, 5, 0], "target": 5}},
        {"in": {"mountainArr": [0, 5, 10, 15, 20, 15, 10, 5, 0], "target": 5}},
        {"in": {"mountainArr": [1, 3, 6, 9, 4, 2], "target": 10}},
        {"in": {"mountainArr": [0, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10], "target": 20}},
        {"in": {"mountainArr": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 5], "target": 5}},
        {"in": {"mountainArr": m1, "target": t1}},
        {"in": {"mountainArr": m2, "target": t2}},
    ]
