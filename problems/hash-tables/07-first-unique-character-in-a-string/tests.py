import random


def visible():
    return [
        {"in": {"s": "leetcode"}},
        {"in": {"s": "loveleetcode"}},
        {"in": {"s": "aabb"}},
    ]


def hidden():
    rng = random.Random(387)
    # Stress 1: unique character at the very last index of a 10,000-char string
    first25 = "abcdefghijklmnopqrstuvwxy"
    stress_last = "".join(rng.choices(first25, k=9999)) + "z"
    # Stress 2: no unique character in a 10,000-char string (all 26 appear many times)
    all26 = "abcdefghijklmnopqrstuvwxyz"
    stress_none = all26 * 2 + "".join(rng.choices(all26, k=9948))

    return [
        {"in": {"s": "z"}},
        {"in": {"s": "zzzzzzzzzz"}},
        {"in": {"s": "aabbccddeeffg"}},
        {"in": {"s": "abccba"}},
        {"in": {"s": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"s": "abcdefghijklmnopqrstuvwxyzyxwvutsrqponmlkjihgfedcba"}},
        {"in": {"s": "dddccdbba"}},
        {"in": {"s": "aadadaad"}},
        {"in": {"s": stress_last}},
        {"in": {"s": stress_none}},
    ]
