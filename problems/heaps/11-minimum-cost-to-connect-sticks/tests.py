import random


def visible():
    return [
        {"in": {"sticks": [2, 4, 3]}},
        {"in": {"sticks": [1, 8, 3, 5]}},
        {"in": {"sticks": [5]}},
    ]


def hidden():
    rng1 = random.Random(116701)
    stress1 = [rng1.randint(1, 10000) for _ in range(3000)]

    # Stress 2: 2000 identical max-length sticks (tests large sum near ~2e8)
    stress2 = [10000] * 2000

    return [
        {"in": {"sticks": [1, 1]}},
        {"in": {"sticks": [10000, 10000]}},
        {"in": {"sticks": [5, 5, 5, 5, 5, 5, 5, 5]}},
        {"in": {"sticks": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
        {"in": {"sticks": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}},
        {"in": {"sticks": [1, 1, 1, 1, 100]}},
        {"in": {"sticks": [3354, 4316, 3259, 4904, 4598, 474, 3166, 6322, 8080, 9009]}},
        {"in": {"sticks": [1, 2, 4, 8, 16, 32, 64, 128]}},
        {"in": {"sticks": stress1}},
        {"in": {"sticks": stress2}},
    ]
