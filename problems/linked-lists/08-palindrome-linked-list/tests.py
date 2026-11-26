import random


def visible():
    return [
        {"in": {"head": [1, 2, 2, 1]}},
        {"in": {"head": [1, 2]}},
        {"in": {"head": [1, 2, 3, 2, 1]}},
    ]


def hidden():
    rng = random.Random(234)
    half_even = [rng.randint(0, 9) for _ in range(2000)]
    stress_pal = half_even + half_even[::-1]
    half_odd = [rng.randint(0, 9) for _ in range(2000)]
    stress_non_pal = half_odd + [5] + half_odd[::-1]
    stress_non_pal[1999] = (stress_non_pal[1999] + 1) % 10
    return [
        {"in": {"head": [7]}},
        {"in": {"head": [5, 5]}},
        {"in": {"head": [1, 2, 3]}},
        {"in": {"head": [0, 9, 0]}},
        {"in": {"head": [0, 0, 0, 0, 0, 0]}},
        {"in": {"head": [1, 2, 3, 4, 3, 2, 0]}},
        {"in": {"head": [1, 2, 3, 4, 5, 3, 2, 1]}},
        {"in": {"head": [1, 2, 3, 9, 4, 2, 1]}},
        {"in": {"head": stress_pal}},
        {"in": {"head": stress_non_pal}},
    ]
