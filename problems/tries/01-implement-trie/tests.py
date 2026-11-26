import random


def visible():
    return [
        {
            "in": {
                "ops": ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
                "args": [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
            }
        },
        {
            "in": {
                "ops": ["Trie", "insert", "insert", "insert", "search", "startsWith", "search", "startsWith", "startsWith"],
                "args": [[], ["cat"], ["car"], ["dog"], ["ca"], ["ca"], ["car"], ["do"], ["bat"]],
            }
        },
    ]


def hidden():
    tests = []

    # 1. Queries on an empty trie
    tests.append({
        "in": {
            "ops": ["Trie", "search", "startsWith", "search", "startsWith"],
            "args": [[], ["a"], ["a"], ["apple"], ["z"]],
        }
    })

    # 2. Single-character words and boundary checks
    tests.append({
        "in": {
            "ops": ["Trie", "insert", "search", "startsWith", "search", "search", "startsWith", "insert", "search"],
            "args": [[], ["a"], ["a"], ["a"], ["b"], ["aa"], ["aa"], ["z"], ["z"]],
        }
    })

    # 3. Duplicate insertions
    tests.append({
        "in": {
            "ops": ["Trie", "insert", "insert", "insert", "search", "search", "startsWith", "startsWith"],
            "args": [[], ["hello"], ["hello"], ["hello"], ["hello"], ["hell"], ["hell"], ["helloo"]],
        }
    })

    # 4. Nested prefix chain inserted longest-first then shortest-first
    tests.append({
        "in": {
            "ops": [
                "Trie", "insert", "search", "search", "startsWith",
                "insert", "search", "search", "insert", "search", "startsWith", "search"
            ],
            "args": [
                [], ["abcde"], ["abcde"], ["abc"], ["abc"],
                ["abc"], ["abc"], ["ab"], ["a"], ["a"], ["abcdef"], ["abcd"]
            ],
        }
    })

    # 5. Diverging words sharing common prefixes
    tests.append({
        "in": {
            "ops": [
                "Trie", "insert", "insert", "insert", "insert",
                "search", "startsWith", "search", "search", "search", "insert", "search", "startsWith"
            ],
            "args": [
                [], ["banana"], ["band"], ["bandana"], ["bank"],
                ["ban"], ["ban"], ["band"], ["bandan"], ["bank"], ["ban"], ["ban"], ["banks"]
            ],
        }
    })

    # 6. Long single word (length 500)
    long_word = "".join(chr(ord("a") + (i % 26)) for i in range(500))
    tests.append({
        "in": {
            "ops": ["Trie", "insert", "startsWith", "startsWith", "search", "search", "startsWith", "search"],
            "args": [
                [], [long_word], [long_word[:1]], [long_word[:250]],
                [long_word[:499]], [long_word], [long_word + "a"], [long_word + "a"]
            ],
        }
    })

    # 7. All 26 lowercase letters inserted
    ops7 = ["Trie"]
    args7 = [[]]
    for i in range(26):
        ch = chr(ord("a") + i)
        ops7.append("insert")
        args7.append([ch])
    for i in range(26):
        ch = chr(ord("a") + i)
        ops7.extend(["search", "startsWith", "search"])
        args7.extend([[ch], [ch], [ch + ch]])
    tests.append({"in": {"ops": ops7, "args": args7}})

    # 8. Repeated identical characters
    tests.append({
        "in": {
            "ops": ["Trie", "insert", "search", "search", "startsWith", "insert", "search", "search", "startsWith"],
            "args": [[], ["aaaa"], ["aaa"], ["aaaa"], ["aaa"], ["aa"], ["aa"], ["aaa"], ["aaaaa"]],
        }
    })

    # 9. Deterministic random mixed workload (400 ops)
    rng = random.Random(20801)
    vocab = ["".join(rng.choice("abcdef") for _ in range(rng.randint(1, 8))) for _ in range(80)]
    ops9 = ["Trie"]
    args9 = [[]]
    for _ in range(400):
        r = rng.random()
        w = rng.choice(vocab)
        if r < 0.35:
            ops9.append("insert")
            args9.append([w])
        elif r < 0.70:
            ops9.append("search")
            args9.append([w if rng.random() < 0.6 else w[:max(1, len(w) - 1)]])
        else:
            ops9.append("startsWith")
            args9.append([w[:rng.randint(1, len(w))]])
    tests.append({"in": {"ops": ops9, "args": args9}})

    # 10. Stress test (1200 ops)
    rng = random.Random(20802)
    prefixes = ["".join(rng.choice("abcdefghij") for _ in range(rng.randint(2, 6))) for _ in range(40)]
    ops10 = ["Trie"]
    args10 = [[]]
    for _ in range(1200):
        base = rng.choice(prefixes)
        suffix = "".join(rng.choice("abcdefghij") for _ in range(rng.randint(0, 6)))
        w = base + suffix
        kind = rng.randint(0, 2)
        if kind == 0:
            ops10.append("insert")
            args10.append([w])
        elif kind == 1:
            ops10.append("search")
            args10.append([w])
        else:
            ops10.append("startsWith")
            args10.append([w[:rng.randint(1, len(w))]])
    tests.append({"in": {"ops": ops10, "args": args10}})

    return tests
