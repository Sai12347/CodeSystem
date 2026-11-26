import random


def visible():
    return [
        {"in": {"s": "aab"}},
        {"in": {"s": "aaab"}},
        {"in": {"s": "aaabbc"}},
    ]


def hidden():
    rng1 = random.Random(76701)
    # Tightly feasible length 499 string: 250 'a's + 249 other chars
    chars1 = ["a"] * 250 + [rng1.choice("bcdefghijklmnopqrstuvwxyz") for _ in range(249)]
    rng1.shuffle(chars1)
    stress_ok = "".join(chars1)

    rng2 = random.Random(76702)
    # Barely impossible length 499 string: 251 'z's + 248 other chars
    chars2 = ["z"] * 251 + [rng2.choice("abcdefghijklmnopqrstuvwxy") for _ in range(248)]
    rng2.shuffle(chars2)
    stress_impossible = "".join(chars2)

    return [
        {"in": {"s": "a"}},
        {"in": {"s": "aa"}},
        {"in": {"s": "ab"}},
        {"in": {"s": "vvvlo"}},
        {"in": {"s": "aabbcc"}},
        {"in": {"s": "aaaaabbbbccc"}},
        {"in": {"s": "zzzzzyyyy"}},
        {"in": {"s": "zzzzzzyyyy"}},
        {"in": {"s": "abcdefghijklmnop"}},
        {"in": {"s": stress_ok}},
        {"in": {"s": stress_impossible}},
    ]
