import random


def visible():
    return [
        {"in": {
            "ops": ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"],
            "args": [[], [1], [2], [2], [], [1], [2], []]
        }},
        {"in": {
            "ops": ["RandomizedSet", "insert", "remove", "insert", "getRandom"],
            "args": [[], [0], [0], [0], []]
        }},
    ]


def hidden():
    rng = random.Random(380)

    # Randomness distribution check: 3 elements, 150 getRandom calls
    ops_rand = ["RandomizedSet", "insert", "insert", "insert"] + ["getRandom"] * 150
    args_rand = [[], [10], [20], [30]] + [[] for _ in range(150)]

    # Stress test: 1500 mixed operations over small key space to cause frequent insert/remove/reinsert
    ops_stress, args_stress = ["RandomizedSet"], [[]]
    present = set()
    for _ in range(1500):
        r = rng.random()
        if not present or r < 0.45:
            val = rng.randint(-50, 50)
            ops_stress.append("insert")
            args_stress.append([val])
            present.add(val)
        elif r < 0.75:
            val = rng.randint(-50, 50)
            ops_stress.append("remove")
            args_stress.append([val])
            present.discard(val)
        else:
            ops_stress.append("getRandom")
            args_stress.append([])

    # Stress test 2: insert 400 elements, remove first 399 (front-swap heavy), query last survivor
    ops_front = ["RandomizedSet"]
    args_front = [[]]
    for i in range(400):
        ops_front.append("insert")
        args_front.append([i])
    for i in range(399):
        ops_front.append("remove")
        args_front.append([i])
        if i % 25 == 0:
            ops_front.append("getRandom")
            args_front.append([])
    ops_front.append("getRandom")
    args_front.append([])

    return [
        # Remove from empty set
        {"in": {
            "ops": ["RandomizedSet", "remove", "remove", "insert", "getRandom", "remove", "insert"],
            "args": [[], [0], [0], [0], [], [0], [0]]
        }},
        # Extreme 32-bit int boundaries
        {"in": {
            "ops": ["RandomizedSet", "insert", "insert", "getRandom", "remove", "getRandom", "remove", "remove"],
            "args": [[], [-2147483648], [2147483647], [], [-2147483648], [], [2147483647], [2147483647]]
        }},
        # Duplicate inserts & removes
        {"in": {
            "ops": ["RandomizedSet", "insert", "insert", "insert", "remove", "remove", "insert", "getRandom"],
            "args": [[], [5], [5], [5], [5], [5], [5], []]
        }},
        # Remove last element vs non-last element swap bug check
        {"in": {
            "ops": ["RandomizedSet", "insert", "insert", "insert", "remove", "remove", "getRandom", "remove", "insert", "getRandom"],
            "args": [[], [1], [2], [3], [3], [1], [], [2], [1], []]
        }},
        # Repeated insert-remove cycles on same elements
        {"in": {
            "ops": ["RandomizedSet", "insert", "insert", "remove", "insert", "remove", "getRandom", "remove", "insert", "getRandom"],
            "args": [[], [-1], [-2], [-2], [-2], [-1], [], [-2], [-1], []]
        }},
        # Negative values only
        {"in": {
            "ops": ["RandomizedSet", "insert", "insert", "insert", "remove", "getRandom", "remove", "getRandom"],
            "args": [[], [-100], [-200], [-300], [-200], [], [-100], []]
        }},
        # Non-trivial randomness test
        {"in": {"ops": ops_rand, "args": args_rand}},
        # Front-heavy removal stress test
        {"in": {"ops": ops_front, "args": args_front}},
        # Mixed random stress test
        {"in": {"ops": ops_stress, "args": args_stress}},
    ]
