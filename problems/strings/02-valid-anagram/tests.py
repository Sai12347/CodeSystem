import random


def _large_anagram(n: int, seed: int, valid: bool) -> tuple[str, str]:
    rng = random.Random(seed)
    chars = [chr(ord("a") + rng.randrange(26)) for _ in range(n)]
    s = "".join(chars)
    shuffled = list(chars)
    rng.shuffle(shuffled)
    if not valid:
        shuffled[n // 2] = "a" if shuffled[n // 2] != "a" else "b"
    t = "".join(shuffled)
    return s, t


def visible():
    return [
        {"in": {"s": "anagram", "t": "nagaram"}},
        {"in": {"s": "rat", "t": "car"}},
        {"in": {"s": "a", "t": "a"}},
    ]


def hidden():
    s1, t1 = _large_anagram(5000, seed=242, valid=True)
    s2, t2 = _large_anagram(5000, seed=243, valid=False)
    return [
        {"in": {"s": "a", "t": "b"}},
        {"in": {"s": "ab", "t": "a"}},
        {"in": {"s": "abc", "t": "abcd"}},
        {"in": {"s": "aacc", "t": "ccac"}},
        {"in": {"s": "ac", "t": "bb"}},
        {"in": {"s": "zzzzzz", "t": "zzzzzz"}},
        {"in": {"s": "abcdefghijklmnopqrstuvwxyz", "t": "zyxwvutsrqponmlkjihgfedcba"}},
        {"in": {"s": "aabbccddeeff", "t": "ffeeddccbbaa"}},
        {"in": {"s": "listen", "t": "silent"}},
        {"in": {"s": s1, "t": t1}},
        {"in": {"s": s2, "t": t2}},
    ]
