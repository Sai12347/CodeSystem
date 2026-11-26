import random


def _make(words, stream):
    return {
        "in": {
            "ops": ["StreamChecker"] + ["query"] * len(stream),
            "args": [[words]] + [[ch] for ch in stream],
        }
    }


def visible():
    return [
        _make(["cd", "f", "kl"], "abcdefghijkl"),
        _make(["ab", "ba", "aaab", "abab", "baa"], "aaaaabababbb"),
    ]


def hidden():
    tests = []

    # 1. Single 1-char word
    tests.append(_make(["a"], "baaba"))

    # 2. Duplicate words in input
    tests.append(_make(["abc", "abc", "bc"], "xabcbc"))

    # 3. Words that are suffixes and prefixes of each other
    tests.append(_make(["c", "bc", "abc", "ab"], "abccbaabc"))

    # 4. Stream never matches any word
    tests.append(_make(["xyz", "pqr", "mnop"], "abcdefghijklmno"))

    # 5. Palindromic words
    tests.append(_make(["aba", "abba", "racecar"], "ababbaxracecar"))

    # 6. Repeated same letter
    tests.append(_make(["aaa", "aaaaa"], "aaaaaaaaba"))

    # 7. Word longer than initial stream, matches on final char
    tests.append(_make(["abcdefghij"], "abcdefghijabcdefghik"))

    # 8. Long word of length 150 matched after near-misses
    w150 = "".join(chr(ord("a") + (i % 5)) for i in range(150))
    stream8 = w150[:149] + "z" + w150 + "a"
    tests.append(_make([w150], stream8))

    # 9. Deterministic test: 100 words, 400 queries
    rng = random.Random(10321)
    words9 = ["".join(rng.choice("abcdef") for _ in range(rng.randint(2, 10))) for _ in range(100)]
    stream9 = "".join(rng.choice("abcdef") for _ in range(400))
    tests.append(_make(words9, stream9))

    # 10. Stress test: 300 words, 1500 queries
    rng = random.Random(10322)
    words10 = ["".join(rng.choice("abcdefgh") for _ in range(rng.randint(2, 20))) for _ in range(300)]
    stream_parts = []
    while sum(len(p) for p in stream_parts) < 1500:
        if rng.random() < 0.2:
            stream_parts.append(rng.choice(words10))
        else:
            stream_parts.append("".join(rng.choice("abcdefgh") for _ in range(rng.randint(5, 25))))
    stream10 = "".join(stream_parts)[:1500]
    tests.append(_make(words10, stream10))

    return tests
