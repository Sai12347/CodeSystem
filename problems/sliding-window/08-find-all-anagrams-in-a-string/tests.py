import random


def visible():
    return [
        {"in": {"s": "cbaebabacd", "p": "abc"}},
        {"in": {"s": "abab", "p": "ab"}},
        {"in": {"s": "abcdef", "p": "xyz"}},
    ]


def hidden():
    rng1 = random.Random(438)
    stress1 = "".join(rng1.choice("abcde") for _ in range(4000))

    stress2 = "ab" * 1500

    return [
        {"in": {"s": "ab", "p": "abc"}},
        {"in": {"s": "a", "p": "a"}},
        {"in": {"s": "a", "p": "b"}},
        {"in": {"s": "aaaaaa", "p": "aaa"}},
        {"in": {"s": "listen", "p": "silent"}},
        {"in": {"s": "listen", "p": "silenx"}},
        {"in": {"s": "baa", "p": "aa"}},
        {"in": {"s": "aabaaabaa", "p": "aab"}},
        {"in": {"s": "zzzzzzcba", "p": "abc"}},
        {"in": {"s": stress1, "p": "abccba"}},
        {"in": {"s": stress2, "p": "aabb"}},
    ]
