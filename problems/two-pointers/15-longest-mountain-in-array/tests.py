import random


def visible():
    return [
        {"in": {"arr": [2, 1, 4, 7, 3, 2, 5]}},
        {"in": {"arr": [2, 2, 2]}},
        {"in": {"arr": [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]}},
    ]


def hidden():
    rng = random.Random(845)

    # Stress test 1: mixed random mountains, flats, and drops (~3000 elements)
    saw = []
    while len(saw) < 3000:
        mode = rng.randint(0, 2)
        if mode == 0:
            up = rng.randint(1, 25)
            down = rng.randint(1, 25)
            start = rng.randint(0, 500)
            for k in range(up):
                saw.append(start + k * 2)
            peak = start + up * 2
            saw.append(peak)
            for k in range(1, down + 1):
                saw.append(max(0, peak - k * 2))
        elif mode == 1:
            val = rng.randint(0, 1000)
            saw.extend([val] * rng.randint(2, 6))
        else:
            saw.extend(rng.randint(0, 10000) for _ in range(rng.randint(3, 10)))
    saw = saw[:3000]

    # Stress test 2: single giant mountain surrounded by flat prefix and suffix
    giant = [5] * 200 + list(range(10, 1910)) + list(range(1908, 8, -1)) + [8] * 200

    return [
        {"in": {"arr": [5]}},
        {"in": {"arr": [1, 2]}},
        {"in": {"arr": [1, 2, 3, 4, 5]}},
        {"in": {"arr": [5, 4, 3, 2, 1]}},
        {"in": {"arr": [1, 2, 3, 3, 2, 1]}},
        {"in": {"arr": [0, 1, 1, 2, 3, 2, 1]}},
        {"in": {"arr": [0, 2, 0, 2, 1, 0]}},
        {"in": {"arr": [5, 4, 3, 2, 1, 2, 1]}},
        {"in": {"arr": saw}},
        {"in": {"arr": giant}},
    ]
