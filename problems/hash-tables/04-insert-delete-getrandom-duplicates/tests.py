import random


def visible():
    return [
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "insert", "getRandom", "remove", "getRandom"],
            "args": [[], [1], [1], [2], [], [1], []]
        }},
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "remove", "remove", "remove", "insert", "getRandom"],
            "args": [[], [5], [5], [5], [5], [5], [5], []]
        }},
    ]


def hidden():
    rng = random.Random(381)

    # Weighted proportionality test: 9 copies of 1 and 1 copy of 2, then 450 getRandom calls
    ops_weighted = ["RandomizedCollection"] + ["insert"] * 9 + ["insert"] + ["getRandom"] * 450
    args_weighted = [[]] + [[1]] * 9 + [[2]] + [[] for _ in range(450)]

    # Stress test: 1500 mixed ops over small key space (heavy duplicates!)
    ops_stress, args_stress = ["RandomizedCollection"], [[]]
    counts = {}
    total = 0
    for _ in range(1500):
        r = rng.random()
        if total == 0 or r < 0.50:
            val = rng.randint(-12, 12)
            ops_stress.append("insert")
            args_stress.append([val])
            counts[val] = counts.get(val, 0) + 1
            total += 1
        elif r < 0.80:
            val = rng.randint(-12, 12)
            ops_stress.append("remove")
            args_stress.append([val])
            if counts.get(val, 0) > 0:
                counts[val] -= 1
                total -= 1
                if counts[val] == 0:
                    del counts[val]
        else:
            ops_stress.append("getRandom")
            args_stress.append([])

    # Same-value tail swap edge-case stress: insert many copies of 1 and 2 interleaved, then remove all 1s
    ops_interleaved = ["RandomizedCollection"]
    args_interleaved = [[]]
    for _ in range(50):
        ops_interleaved.extend(["insert", "insert", "insert"])
        args_interleaved.extend([[1], [2], [1]])
    for _ in range(100):
        ops_interleaved.append("remove")
        args_interleaved.append([1])
    ops_interleaved.extend(["remove", "getRandom", "getRandom"])
    args_interleaved.extend([[1], [], []])

    return [
        # Remove from empty
        {"in": {
            "ops": ["RandomizedCollection", "remove", "insert", "remove", "remove", "insert", "getRandom"],
            "args": [[], [0], [0], [0], [0], [0], []]
        }},
        # Classic LC 381 tricky swap case: insert 1, 1, 2, 2, 2, remove 1, 1, 2, insert 1, remove 2
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "insert", "insert", "insert",
                    "remove", "remove", "remove", "insert", "remove", "getRandom"],
            "args": [[], [1], [1], [2], [2], [2], [1], [1], [2], [1], [2], []]
        }},
        # Removing last element when duplicate exists earlier: [1, 2, 1] remove(1)
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "insert", "remove", "remove", "getRandom"],
            "args": [[], [1], [2], [1], [1], [1], []]
        }},
        # Extreme 32-bit int values with duplicates
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "insert", "remove", "getRandom", "remove", "getRandom"],
            "args": [[], [-2147483648], [-2147483648], [2147483647], [-2147483648], [], [-2147483648], []]
        }},
        # Drain completely to empty then refill
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "remove", "remove", "insert", "insert", "getRandom", "remove", "getRandom"],
            "args": [[], [10], [20], [10], [20], [30], [30], [], [30], []]
        }},
        # Multiple distinct values removed in reverse insertion order
        {"in": {
            "ops": ["RandomizedCollection", "insert", "insert", "insert", "insert", "remove", "remove", "remove", "getRandom"],
            "args": [[], [4], [3], [4], [2], [4], [3], [4], []]
        }},
        # Weighted proportionality check
        {"in": {"ops": ops_weighted, "args": args_weighted}},
        # Interleaved same-value tail swaps
        {"in": {"ops": ops_interleaved, "args": args_interleaved}},
        # Heavy random stress test
        {"in": {"ops": ops_stress, "args": args_stress}},
    ]
