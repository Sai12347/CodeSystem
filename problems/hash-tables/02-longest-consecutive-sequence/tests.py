import random


def visible():
    return [
        {"in": {"nums": [100, 4, 200, 1, 3, 2]}},
        {"in": {"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}},
        {"in": {"nums": []}},
    ]


def hidden():
    rng = random.Random(128)
    # Stress test 1: shuffled multiple chains + duplicates
    stress1 = []
    for start, length in [(-50000, 400), (1000, 950), (500000, 300), (-999999999, 250)]:
        stress1.extend(range(start, start + length))
    stress1.extend([1000] * 300)  # heavy duplicate start trap
    stress1.extend(rng.randint(-10**9, 10**9) for _ in range(800))
    rng.shuffle(stress1)

    # Stress test 2: dense random values in narrow band
    stress2 = [rng.randint(-1000, 1000) for _ in range(4000)]

    return [
        {"in": {"nums": [42]}},
        {"in": {"nums": [7, 7, 7, 7, 7]}},
        {"in": {"nums": [1, 3, 5, 7, 9, 11]}},
        {"in": {"nums": [-5, -4, -3, -2, -1, 0, 1, 2]}},
        {"in": {"nums": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"nums": [-1000000000, -999999999, -999999998, 999999998, 999999999, 1000000000]}},
        {"in": {"nums": [1, 2, 0, 1]}},
        {"in": {"nums": [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]}},
        {"in": {"nums": [10, 11, 12, 20, 21, 22, 30, 31, 32]}},
        {"in": {"nums": stress1}},
        {"in": {"nums": stress2}},
    ]
