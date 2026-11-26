import random


def visible():
    return [
        {"in": {"heightMap": [
            [1, 4, 3, 1, 3, 2],
            [3, 2, 1, 3, 2, 4],
            [2, 3, 3, 2, 3, 1],
        ]}},
        {"in": {"heightMap": [
            [3, 3, 3, 3, 3],
            [3, 2, 2, 2, 3],
            [3, 2, 1, 2, 3],
            [3, 2, 2, 2, 3],
            [3, 3, 3, 3, 3],
        ]}},
        {"in": {"heightMap": [[5, 1], [2, 8]]}},
    ]


def hidden():
    rng1 = random.Random(40701)
    stress1 = [[rng1.randint(0, 50) for _ in range(30)] for _ in range(30)]

    # Stress 2: bowl with tall rim and noisy interior
    rng2 = random.Random(40702)
    stress2 = [[20000 if (r in (0, 24) or c in (0, 24)) else rng2.randint(0, 15000) for c in range(25)] for r in range(25)]
    stress2[0][12] = 12000  # spillway notch on rim

    return [
        {"in": {"heightMap": [[10]]}},
        {"in": {"heightMap": [[3, 0, 2, 0, 4]]}},
        {"in": {"heightMap": [[3], [0], [2], [0], [4]]}},
        {"in": {"heightMap": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]}},
        # Leaky corner vs solid orthogonal walls: diagonals do NOT leak!
        {"in": {"heightMap": [
            [0, 5, 0],
            [5, 1, 5],
            [0, 5, 0],
        ]}},
        # Single leak channel draining an otherwise deep pool
        {"in": {"heightMap": [
            [9, 9, 9, 9, 9],
            [9, 1, 1, 1, 9],
            [9, 1, 2, 1, 2],
            [9, 1, 1, 1, 9],
            [9, 9, 9, 9, 9],
        ]}},
        # Two separate basins with different spill heights
        {"in": {"heightMap": [
            [10, 10, 10, 10, 10, 10, 10],
            [10, 2, 2, 10, 1, 1, 6],
            [10, 2, 2, 10, 1, 1, 10],
            [10, 8, 10, 10, 10, 10, 10],
        ]}},
        # Tall inner pillar surrounded by moat
        {"in": {"heightMap": [
            [5, 5, 5, 5, 5],
            [5, 1, 1, 1, 5],
            [5, 1, 9, 1, 5],
            [5, 1, 1, 1, 5],
            [5, 5, 5, 5, 5],
        ]}},
        {"in": {"heightMap": stress1}},
        {"in": {"heightMap": stress2}},
    ]
