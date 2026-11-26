import random


def visible():
    return [
        {
            "in": {
                "words": [
                    "cat", "cats", "catsdogcats", "dog", "dogcatsdog",
                    "hippopotamuses", "rat", "ratcatdogcat"
                ]
            }
        },
        {
            "in": {
                "words": ["cat", "dog", "catdog"]
            }
        },
    ]


def hidden():
    tests = []

    # 1. Single word
    tests.append({"in": {"words": ["a"]}})

    # 2. No concatenated words
    tests.append({"in": {"words": ["abc", "def", "ghi", "jkl", "mno"]}})

    # 3. Same word repeated multiple times
    tests.append({"in": {"words": ["a", "aa", "aaa", "aaaa", "aaaaa"]}})

    # 4. Memoization trap (repeated 'a' ending with 'b' fails)
    tests.append({
        "in": {
            "words": [
                "a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaab",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ]
        }
    })

    # 5. Backtracking required (greedy longest match fails)
    tests.append({
        "in": {
            "words": ["ab", "abc", "cd", "abcd", "bc", "def", "abcdef", "abce"]
        }
    })

    # 6. Reverse length order input
    tests.append({
        "in": {
            "words": ["sunflowerpot", "flowerpot", "sunflower", "flower", "pot", "sun", "moonlight", "moon"]
        }
    })

    # 7. Multi-part concatenation (4+ words)
    tests.append({
        "in": {
            "words": ["a", "b", "c", "d", "abcd", "dcba", "ab", "cd", "ababab", "abce"]
        }
    })

    # 8. Overlapping prefixes with zero valid concatenations
    tests.append({
        "in": {
            "words": ["a", "ab", "abc", "abcd", "abcde", "xyz", "xyzw"]
        }
    })

    # 9. Deterministic synthetic dictionary (250 words)
    rng = random.Random(47201)
    bases = set()
    while len(bases) < 60:
        bases.add("".join(rng.choice("abcdefgh") for _ in range(rng.randint(2, 5))))
    base_list = sorted(bases)
    words9 = set(base_list)
    for _ in range(120):
        parts = [rng.choice(base_list) for _ in range(rng.randint(2, 4))]
        w = "".join(parts)
        if len(w) <= 30:
            words9.add(w)
    while len(words9) < 250:
        words9.add("".join(rng.choice("abcdefgh") for _ in range(rng.randint(5, 15))))
    w9_list = list(words9)
    rng.shuffle(w9_list)
    tests.append({"in": {"words": w9_list}})

    # 10. Stress test (900 words including memoization traps)
    rng = random.Random(47202)
    bases10 = set()
    while len(bases10) < 120:
        bases10.add("".join(rng.choice("abcdef") for _ in range(rng.randint(2, 5))))
    base10_list = sorted(bases10)
    words10 = set(base10_list)
    for k in range(1, 8):
        words10.add("x" * k)
    words10.add("x" * 29 + "y")
    words10.add("x" * 30)
    for _ in range(450):
        parts = [rng.choice(base10_list) for _ in range(rng.randint(2, 5))]
        w = "".join(parts)
        if len(w) <= 30:
            words10.add(w)
    while len(words10) < 900:
        words10.add("".join(rng.choice("abcdef") for _ in range(rng.randint(6, 20))))
    w10_list = list(words10)
    rng.shuffle(w10_list)
    tests.append({"in": {"words": w10_list}})

    return tests
