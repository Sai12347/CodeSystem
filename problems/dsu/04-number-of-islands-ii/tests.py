import random


def _gen_positions(m: int, n: int, k: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randrange(m), rng.randrange(n)] for _ in range(k)]


def visible():
    return [
        {"in": {"m": 3, "n": 3, "positions": [[0, 0], [0, 1], [1, 2], [2, 1]]}},
        {"in": {"m": 1, "n": 1, "positions": [[0, 0]]}},
    ]


def hidden():
    # 1. Empty operations list
    t1 = (3, 3, [])
    # 2. Duplicate positions mixed with merges
    t2 = (3, 3, [[0, 0], [0, 1], [1, 2], [1, 2], [0, 0], [2, 1], [1, 1], [1, 1]])
    # 3. Four-way simultaneous merge into a single island
    t3 = (3, 3, [[0, 1], [1, 0], [1, 2], [2, 1], [1, 1]])
    # 4. 1D horizontal strip: fill evens then bridge with odds
    t4 = (1, 10, [[0, c] for c in range(0, 10, 2)] + [[0, c] for c in range(1, 10, 2)])
    # 5. 1D vertical strip: fill evens then bridge with odds
    t5 = (10, 1, [[r, 0] for r in range(0, 10, 2)] + [[r, 0] for r in range(1, 10, 2)])
    # 6. 4x4 checkerboard (diagonals must not merge), then fill remaining cells
    evens = [[r, c] for r in range(4) for c in range(4) if (r + c) % 2 == 0]
    odds = [[r, c] for r in range(4) for c in range(4) if (r + c) % 2 == 1]
    t6 = (4, 4, evens + odds)
    # 7. Spiral inward on 5x5 grid
    spiral = []
    top, bot, left, right = 0, 4, 0, 4
    while top <= bot and left <= right:
        for c in range(left, right + 1):
            spiral.append([top, c])
        top += 1
        for r in range(top, bot + 1):
            spiral.append([r, right])
        right -= 1
        if top <= bot:
            for c in range(right, left - 1, -1):
                spiral.append([bot, c])
            bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1):
                spiral.append([r, left])
            left += 1
    t7 = (5, 5, spiral)
    # 8. Extreme rectangular 1 x 10000 grid
    t8 = (1, 10000, [[0, 0], [0, 9999], [0, 5000], [0, 1], [0, 9998], [0, 5000], [0, 4999], [0, 5001]])
    # 9. Medium random grid with duplicates
    t9 = (30, 30, _gen_positions(30, 30, 300, 3051))
    # 10. Stress test: 100 x 100 grid with 1500 random operations
    t10 = (100, 100, _gen_positions(100, 100, 1500, 3052))

    return [
        {"in": {"m": m, "n": n, "positions": pos}}
        for m, n, pos in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)
    ]
