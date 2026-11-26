import random


def visible():
    return [
        {"in": {"nums": [1, 7, 3, 6, 5, 6]}},
        {"in": {"nums": [1, 2, 3]}},
        {"in": {"nums": [2, 1, -1]}},
    ]


def hidden():
    rng = random.Random(724)
    # Construct a large symmetric array with a guaranteed pivot in the middle
    half = [rng.randint(-1000, 1000) for _ in range(999)]
    sym_big = half + [777] + half[::-1]
    # Construct a large array with no pivot (strictly positive except huge last element)
    no_pivot_big = [1] * 1500 + [999]
    # Construct a large array with pivot at the very last index
    left_zero = [rng.randint(-500, 500) for _ in range(400)]
    pivot_at_end = left_zero + [-x for x in left_zero] + [42]
    return [
        {"in": {"nums": [0]}},
        {"in": {"nums": [99]}},
        {"in": {"nums": [-1, 1, 2]}},
        {"in": {"nums": [0, 0, 0, 0]}},
        {"in": {"nums": [-1, -1, -1, -1, -1, 0]}},
        {"in": {"nums": [-1, -1, -1, 0, 1, 1]}},
        {"in": {"nums": [1, -1, 1, -1, 1, -1, 5]}},
        {"in": {"nums": [1000, -1000, 1000, -1000]}},
        {"in": {"nums": [1, 2, 3, 4, 5, 4, 3, 2, 1]}},
        {"in": {"nums": pivot_at_end}},
        {"in": {"nums": no_pivot_big}},
        {"in": {"nums": sym_big}},
    ]
