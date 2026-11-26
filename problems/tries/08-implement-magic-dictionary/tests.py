import random


def visible():
    return [
        {
            "in": {
                "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search"],
                "args": [[], [["hello", "leetcode"]], ["hello"], ["hhllo"], ["hell"], ["leetcoded"]],
            }
        },
        {
            "in": {
                "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search"],
                "args": [[], [["hello", "hallo", "leetcode"]], ["hello"], ["hhllo"], ["hell"], ["leetcoded"]],
            }
        },
    ]


def hidden():
    tests = []

    # 1. Single-character dictionary
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search"],
            "args": [[], [["a"]], ["a"], ["b"], ["z"], ["ab"]],
        }
    })

    # 2. Two single-character words
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search"],
            "args": [[], [["a", "b"]], ["a"], ["b"], ["c"]],
        }
    })

    # 3. Single difference at first, middle, and last positions
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search", "search"],
            "args": [[], [["apple"]], ["xpple"], ["apxle"], ["applx"], ["apple"], ["xpply"]],
        }
    })

    # 4. Two-character differences must fail
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search"],
            "args": [[], [["abcde", "fghij"]], ["axcye"], ["fbcde"], ["abcfg"], ["fghix"]],
        }
    })

    # 5. Prefix / superstring length traps
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search", "search"],
            "args": [[], [["ab", "abc", "abcd"]], ["ab"], ["abc"], ["abd"], ["abce"], ["a"]],
        }
    })

    # 6. Many same-length words with tight branching
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search", "search", "search"],
            "args": [
                [], [["aaaa", "aaba", "abaa", "baaa", "cccc"]],
                ["aaaa"], ["aaab"], ["bbbb"], ["cccd"], ["ccdd"], ["abba"]
            ],
        }
    })

    # 7. Max length boundary (length 100)
    w100 = "a" * 100
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search", "search"],
            "args": [
                [], [[w100]],
                [w100],
                ["b" + w100[1:]],
                [w100[:50] + "z" + w100[51:]],
                [w100[:99] + "c"],
                ["b" + w100[1:99] + "c"],
            ],
        }
    })

    # 8. Repeated letters and exact-match vs neighbor
    tests.append({
        "in": {
            "ops": ["MagicDictionary", "buildDict", "search", "search", "search", "search"],
            "args": [[], [["zzz", "zzx", "yyy"]], ["zzz"], ["zzx"], ["yyy"], ["yxy"]],
        }
    })

    # 9. Deterministic random test (50 words, 60 searches)
    rng = random.Random(67601)
    d9 = set()
    while len(d9) < 50:
        d9.add("".join(rng.choice("abcdef") for _ in range(rng.randint(3, 10))))
    d9_list = sorted(d9)
    ops9 = ["MagicDictionary", "buildDict"]
    args9 = [[], [d9_list]]
    for _ in range(60):
        base = list(rng.choice(d9_list))
        mode = rng.randint(0, 3)
        if mode == 1:
            pos = rng.randrange(len(base))
            choices = [c for c in "abcdefg" if c != base[pos]]
            base[pos] = rng.choice(choices)
        elif mode == 2 and len(base) >= 2:
            for pos in rng.sample(range(len(base)), 2):
                choices = [c for c in "abcdefg" if c != base[pos]]
                base[pos] = rng.choice(choices)
        elif mode == 3:
            base.append("a")
        ops9.append("search")
        args9.append(["".join(base)])
    tests.append({"in": {"ops": ops9, "args": args9}})

    # 10. Stress test: max 100 words of length 15..40, 100 searches
    rng = random.Random(67602)
    d10 = set()
    while len(d10) < 100:
        d10.add("".join(rng.choice("abcdefghij") for _ in range(rng.randint(15, 40))))
    d10_list = sorted(d10)
    ops10 = ["MagicDictionary", "buildDict"]
    args10 = [[], [d10_list]]
    for _ in range(100):
        base = list(rng.choice(d10_list))
        mode = rng.randint(0, 2)
        if mode == 1:
            pos = rng.randrange(len(base))
            base[pos] = "z"
        elif mode == 2:
            for pos in rng.sample(range(len(base)), 2):
                base[pos] = "z"
        ops10.append("search")
        args10.append(["".join(base)])
    tests.append({"in": {"ops": ops10, "args": args10}})

    return tests
