import random


def visible():
    return [
        {"in": {"numbers": [2, 7, 11, 15], "target": 9}},
        {"in": {"numbers": [2, 3, 4], "target": 6}},
        {"in": {"numbers": [-1, 0], "target": -1}},
    ]


def hidden():
    rng = random.Random(167)
    # Construct a large random sorted array with a mathematically guaranteed unique pair:
    # all distractor values are multiples of 5, while the two answer elements are 1 and 2 (mod 5),
    # so only their pair sums to 3 (mod 5).
    distractors = [rng.randint(-200, 200) * 5 for _ in range(1998)]
    a, b = -374, 627  # a % 5 == 1, b % 5 == 2, a + b == 253 (% 5 == 3)
    big_rand = sorted(distractors + [a, b])

    # Adversarial test where converging pointers must scan from both ends to the middle
    middle_meet = [-1000] * 1500 + [-100, 101] + [1000] * 1500

    return [
        {"in": {"numbers": [0, 0], "target": 0}},
        {"in": {"numbers": [0, 0, 3, 4], "target": 0}},
        {"in": {"numbers": [-15, -8, -4, -2, -1], "target": -12}},
        {"in": {"numbers": [-1000, -500, 0, 500, 1000], "target": 1000}},
        {"in": {"numbers": [-1000, -500, -1, 0, 500, 1000], "target": -1000}},
        {"in": {"numbers": [-100, -50, -20, 3, 4, 20, 50, 100], "target": 7}},
        {"in": {"numbers": [1, 2, 4, 8, 16, 32, 64, 128], "target": 96}},
        {"in": {"numbers": [-500, -250, -125, -60, -10, 5, 40, 120, 300, 600], "target": 100}},
        {"in": {"numbers": middle_meet, "target": 1}},
        {"in": {"numbers": big_rand, "target": a + b}},
    ]
