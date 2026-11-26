import random


def visible():
    return [
        {"in": {"s1": "ab", "s2": "eidbaooo"}},
        {"in": {"s1": "ab", "s2": "eidboaoo"}},
        {"in": {"s1": "adc", "s2": "dcda"}},
    ]


def hidden():
    rng = random.Random(567)
    alpha = "abcdefghijklmnopqrstuvwxyz"

    # Stress test 1: true match buried near the end of a large string
    s1_large = "".join(rng.choice(alpha[:8]) for _ in range(250))
    perm = list(s1_large)
    rng.shuffle(perm)
    prefix = "".join(rng.choice(alpha[:8]) for _ in range(2400))
    suffix = "".join(rng.choice(alpha[:8]) for _ in range(150))
    s2_true = prefix + "".join(perm) + suffix

    # Stress test 2: off-by-one near-miss across every window
    s1_miss = "a" * 101 + "b" * 99
    s2_miss = "ab" * 1200

    return [
        {"in": {"s1": "a", "s2": "a"}},
        {"in": {"s1": "a", "s2": "b"}},
        {"in": {"s1": "abcd", "s2": "abc"}},
        {"in": {"s1": "xyz", "s2": "zyxabcdef"}},
        {"in": {"s1": "xyz", "s2": "abcdefzyx"}},
        {"in": {"s1": "aabb", "s2": "aaabbb"}},
        {"in": {"s1": "aab", "s2": "cbaba"}},
        {"in": {"s1": "zzzz", "s2": "zzzzzz"}},
        {"in": {"s1": s1_large, "s2": s2_true}},
        {"in": {"s1": s1_miss, "s2": s2_miss}},
    ]
