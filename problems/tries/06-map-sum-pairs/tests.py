import random


def visible():
    return [
        {
            "in": {
                "ops": ["MapSum", "insert", "sum", "insert", "sum"],
                "args": [[], ["apple", 3], ["ap"], ["app", 2], ["ap"]],
            }
        },
        {
            "in": {
                "ops": ["MapSum", "insert", "sum", "insert", "insert", "sum", "sum"],
                "args": [[], ["apple", 3], ["ap"], ["app", 2], ["apple", 5], ["ap"], ["apple"]],
            }
        },
    ]


def hidden():
    tests = []

    # 1. Empty map queries
    tests.append({
        "in": {
            "ops": ["MapSum", "sum", "sum"],
            "args": [[], ["a"], ["hello"]],
        }
    })

    # 2. Overwrite with smaller value (negative delta)
    tests.append({
        "in": {
            "ops": ["MapSum", "insert", "insert", "sum", "insert", "sum", "sum"],
            "args": [[], ["apple", 100], ["app", 50], ["ap"], ["apple", 10], ["ap"], ["appl"]],
        }
    })

    # 3. Overwrite with identical value (zero delta)
    tests.append({
        "in": {
            "ops": ["MapSum", "insert", "sum", "insert", "sum"],
            "args": [[], ["code", 42], ["co"], ["code", 42], ["co"]],
        }
    })

    # 4. Nested prefix chain with overwrites
    tests.append({
        "in": {
            "ops": [
                "MapSum", "insert", "insert", "insert", "insert",
                "sum", "sum", "sum", "sum", "insert", "sum", "sum"
            ],
            "args": [
                [], ["a", 1], ["aa", 2], ["aaa", 3], ["aaaa", 4],
                ["a"], ["aa"], ["aaa"], ["aaaa"], ["aa", 20], ["a"], ["aaa"]
            ],
        }
    })

    # 5. Disjoint prefixes and prefixes longer than any key
    tests.append({
        "in": {
            "ops": ["MapSum", "insert", "insert", "insert", "sum", "sum", "sum", "sum"],
            "args": [[], ["cat", 7], ["car", 13], ["dog", 20], ["ca"], ["cats"], ["do"], ["z"]],
        }
    })

    # 6. Single-character keys
    tests.append({
        "in": {
            "ops": ["MapSum", "insert", "insert", "insert", "sum", "sum", "insert", "sum"],
            "args": [[], ["a", 10], ["b", 20], ["ab", 5], ["a"], ["b"], ["a", 1], ["a"]],
        }
    })

    # 7. Max length keys (length 50) sharing a 49-char prefix
    p49 = "a" * 49
    tests.append({
        "in": {
            "ops": ["MapSum", "insert", "insert", "sum", "sum", "sum", "insert", "sum"],
            "args": [[], [p49 + "a", 500], [p49 + "b", 600], [p49], [p49 + "a"], [p49 + "c"], [p49 + "a", 1000], [p49]],
        }
    })

    # 8. Repeated overwrites on same key alongside siblings
    tests.append({
        "in": {
            "ops": [
                "MapSum", "insert", "insert", "insert", "insert", "insert", "sum", "sum", "sum"
            ],
            "args": [
                [], ["tree", 5], ["trie", 10], ["tree", 15], ["tree", 1], ["try", 9],
                ["tr"], ["tre"], ["tri"]
            ],
        }
    })

    # 9. Deterministic random workload (300 ops)
    rng = random.Random(67701)
    keys = ["".join(rng.choice("abcde") for _ in range(rng.randint(1, 8))) for _ in range(60)]
    ops9 = ["MapSum"]
    args9 = [[]]
    for _ in range(300):
        k = rng.choice(keys)
        if rng.random() < 0.55:
            ops9.append("insert")
            args9.append([k, rng.randint(1, 1000)])
        else:
            ops9.append("sum")
            args9.append([k[:rng.randint(1, len(k))]])
    tests.append({"in": {"ops": ops9, "args": args9}})

    # 10. Stress test (800 ops)
    rng = random.Random(67702)
    prefixes = ["".join(rng.choice("abcdefgh") for _ in range(rng.randint(2, 6))) for _ in range(30)]
    keys10 = [rng.choice(prefixes) + "".join(rng.choice("abcdefgh") for _ in range(rng.randint(0, 6))) for _ in range(150)]
    ops10 = ["MapSum"]
    args10 = [[]]
    for _ in range(800):
        k = rng.choice(keys10)
        if rng.random() < 0.5:
            ops10.append("insert")
            args10.append([k, rng.randint(1, 1000)])
        else:
            ops10.append("sum")
            args10.append([k[:rng.randint(1, len(k))]])
    tests.append({"in": {"ops": ops10, "args": args10}})

    return tests
