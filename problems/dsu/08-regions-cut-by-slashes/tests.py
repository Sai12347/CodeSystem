import random


def _gen_grid(n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    chars = ["/", "\\", " "]
    return ["".join(rng.choice(chars) for _ in range(n)) for _ in range(n)]


def visible():
    return [
        {"in": {"grid": [" /", "/ "]}},
        {"in": {"grid": [" /", "  "]}},
        {"in": {"grid": ["/\\", "\\/"]}},
    ]


def hidden():
    # 1. 1x1 blank
    t1 = [" "]
    # 2. 1x1 forward slash
    t2 = ["/"]
    # 3. 1x1 backslash
    t3 = ["\\"]
    # 4. 2x2 X-pattern (no enclosed center diamond -> 4 regions)
    t4 = ["\\/", "/\\"]
    # 5. 3x3 all spaces -> 1 region
    t5 = ["   ", "   ", "   "]
    # 6. 4x4 all forward slashes
    t6 = ["////"] * 4
    # 7. 4x4 all backslashes
    t7 = ["\\\\\\\\"] * 4
    # 8. 4x4 checkerboard of '/' and '\' forming multiple enclosed diamonds
    t8 = ["/\\/\\", "\\/\\/", "/\\/\\", "\\/\\/"]
    # 9. Medium random 12x12 grid
    t9 = _gen_grid(12, 9591)
    # 10. Max-size 30x30 stress test
    t10 = _gen_grid(30, 9592)

    return [{"in": {"grid": t}} for t in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
