import random


def visible():
    return [
        {"in": {"l1": [2, 4, 3], "l2": [5, 6, 4]}},
        {"in": {"l1": [0], "l2": [0]}},
        {"in": {"l1": [9, 9, 9, 9, 9, 9, 9], "l2": [9, 9, 9, 9]}},
    ]


def hidden():
    rng = random.Random(2)

    def rand_num(length):
        digits = [rng.randint(0, 9) for _ in range(length - 1)]
        digits.append(rng.randint(1, 9))
        return digits

    return [
        # Single digit without carry
        {"in": {"l1": [1], "l2": [2]}},
        # Single digit with carry
        {"in": {"l1": [5], "l2": [5]}},
        # Adding zero to a multi-digit number
        {"in": {"l1": [0], "l2": [1, 2, 3, 4, 5]}},
        # Cascading carry across all 9s (l1 longer)
        {"in": {"l1": [9, 9, 9, 9, 9], "l2": [1]}},
        # Cascading carry across all 9s (l2 longer)
        {"in": {"l1": [1], "l2": [9, 9, 9, 9, 9]}},
        # Alternating carries
        {"in": {"l1": [5, 4, 5, 4, 5], "l2": [5, 5, 5, 5, 5]}},
        # Exceeds 64-bit signed integer range (25 digits + 25 digits)
        {"in": {"l1": rand_num(25), "l2": rand_num(25)}},
        # Max length 100 all 9s + 1 -> 101 digits
        {"in": {"l1": [9] * 100, "l2": [1]}},
        # Max length 100 all 9s + max length 100 all 9s
        {"in": {"l1": [9] * 100, "l2": [9] * 100}},
        # Stress: max length 100 + 87 random digits
        {"in": {"l1": rand_num(100), "l2": rand_num(87)}},
    ]
