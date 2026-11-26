import random


def visible():
    return [
        {"in": {"s": "abc"}},
        {"in": {"s": "aaa"}},
        {"in": {"s": "abba"}},
    ]


def hidden():
    rng = random.Random(647)
    stress_rand = "".join(rng.choice("abc") for _ in range(1000))
    return [
        {"in": {"s": "a"}},
        {"in": {"s": "zz"}},
        {"in": {"s": "ab"}},
        {"in": {"s": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"s": "racecar"}},
        {"in": {"s": "ababababa"}},
        {"in": {"s": "abacaba"}},
        {"in": {"s": "aabbaabb"}},
        {"in": {"s": "a" * 1000}},
        {"in": {"s": stress_rand}},
    ]
