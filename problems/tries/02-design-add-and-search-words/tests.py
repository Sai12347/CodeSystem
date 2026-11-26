import random


def visible():
    return [
        {
            "in": {
                "ops": ["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"],
                "args": [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]],
            }
        },
        {
            "in": {
                "ops": ["WordDictionary", "addWord", "addWord", "search", "search", "search", "search", "search", "search"],
                "args": [[], ["a"], ["ab"], ["."], [".."], ["..."], ["a."], [".b"], ["a"]],
            }
        },
    ]


def hidden():
    tests = []

    # 1. Empty dictionary searches
    tests.append({
        "in": {
            "ops": ["WordDictionary", "search", "search", "search"],
            "args": [[], ["a"], ["."], [".."]],
        }
    })

    # 2. Single-character words and wildcards
    tests.append({
        "in": {
            "ops": ["WordDictionary", "addWord", "search", "search", "search", "search", "addWord", "search"],
            "args": [[], ["m"], ["m"], ["."], ["n"], [".."], ["n"], ["n"]],
        }
    })

    # 3. Duplicate additions
    tests.append({
        "in": {
            "ops": ["WordDictionary", "addWord", "addWord", "search", "search", "search"],
            "args": [[], ["code"], ["code"], ["code"], ["c.d."], ["cod"]],
        }
    })

    # 4. Prefix vs complete word traps
    tests.append({
        "in": {
            "ops": ["WordDictionary", "addWord", "search", "search", "search", "search", "addWord", "search", "search"],
            "args": [[], ["apple"], ["app"], ["ap."], ["app.."], ["appl."], ["app"], ["app"], ["ap."]],
        }
    })

    # 5. Up to 3 wildcards in various positions
    tests.append({
        "in": {
            "ops": [
                "WordDictionary", "addWord", "addWord", "addWord",
                "search", "search", "search", "search", "search", "search"
            ],
            "args": [
                [], ["abcde"], ["axcye"], ["xyz"],
                ["..."], ["a.c.e"], [".b.d."], ["a.c.z"], ["..c.."], ["x.z"]
            ],
        }
    })

    # 6. Backtracking across sibling branches
    tests.append({
        "in": {
            "ops": [
                "WordDictionary", "addWord", "addWord", "addWord",
                "search", "search", "search", "search", "search"
            ],
            "args": [
                [], ["abcde"], ["abxfg"], ["abzfg"],
                ["ab.fg"], ["ab.de"], ["ab.dg"], ["ab..g"], ["a..de"]
            ],
        }
    })

    # 7. Max length boundary (length 25)
    w25a = "abcdefghijklmnopqrstuvwxy"
    w25b = "abcdefghijklxnopqrstuvwxy"
    tests.append({
        "in": {
            "ops": ["WordDictionary", "addWord", "search", "search", "search", "search", "addWord", "search"],
            "args": [
                [], [w25a], [w25a], ["." + w25a[1:]], [w25a[:12] + "." + w25a[13:]],
                [w25b], [w25b], [w25a[:12] + "." + w25a[13:24] + "."]
            ],
        }
    })

    # 8. Mixed lengths with all-dot queries
    tests.append({
        "in": {
            "ops": [
                "WordDictionary", "addWord", "addWord", "addWord",
                "search", "search", "search", "search", "search"
            ],
            "args": [
                [], ["a"], ["bcd"], ["efghij"],
                ["."], [".."], ["..."], ["e.g.i."], ["e.g.z."]
            ],
        }
    })

    # 9. Deterministic mixed random workload (350 ops, <= 2 dots)
    rng = random.Random(21101)
    alphabet = "abcdefg"
    added = []
    ops9 = ["WordDictionary"]
    args9 = [[]]
    for _ in range(350):
        if not added or rng.random() < 0.4:
            w = "".join(rng.choice(alphabet) for _ in range(rng.randint(2, 8)))
            added.append(w)
            ops9.append("addWord")
            args9.append([w])
        else:
            base = list(rng.choice(added)) if rng.random() < 0.65 else [rng.choice(alphabet) for _ in range(rng.randint(2, 8))]
            num_dots = rng.randint(0, min(2, len(base)))
            for idx in rng.sample(range(len(base)), num_dots):
                base[idx] = "."
            ops9.append("search")
            args9.append(["".join(base)])
    tests.append({"in": {"ops": ops9, "args": args9}})

    # 10. Stress test (1000 ops, <= 2 dots)
    rng = random.Random(21102)
    alphabet = "abcdefghij"
    added = []
    ops10 = ["WordDictionary"]
    args10 = [[]]
    for _ in range(1000):
        if len(added) < 20 or rng.random() < 0.45:
            w = "".join(rng.choice(alphabet) for _ in range(rng.randint(3, 12)))
            added.append(w)
            ops10.append("addWord")
            args10.append([w])
        else:
            base = list(rng.choice(added)) if rng.random() < 0.6 else [rng.choice(alphabet) for _ in range(rng.randint(3, 12))]
            if rng.random() < 0.25:
                base[rng.randrange(len(base))] = rng.choice(alphabet)
            num_dots = rng.randint(0, min(2, len(base)))
            for idx in rng.sample(range(len(base)), num_dots):
                base[idx] = "."
            ops10.append("search")
            args10.append(["".join(base)])
    tests.append({"in": {"ops": ops10, "args": args10}})

    return tests
