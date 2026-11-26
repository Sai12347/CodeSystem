import random


def visible():
    return [
        {"in": {"s": "aba"}},
        {"in": {"s": "abca"}},
        {"in": {"s": "abc"}},
    ]


def hidden():
    rng1 = random.Random(701)
    half1 = "".join(rng1.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(2000))
    stress_true = half1[:1234] + "z" + half1[1234:] + half1[::-1]

    rng2 = random.Random(702)
    half2 = "".join(rng2.choice("abcdefgh") for _ in range(2000))
    # Insert two distinct mismatches far apart so one deletion cannot repair both
    stress_false = half2[:500] + "x" + half2[500:1500] + "y" + half2[1500:] + half2[::-1]

    return [
        {"in": {"s": "z"}},
        {"in": {"s": "ab"}},
        {"in": {"s": "aaaaaaaaaa"}},
        {"in": {"s": "xracecar"}},
        {"in": {"s": "racecarx"}},
        {"in": {"s": "abccbca"}},
        {"in": {"s": "acbccba"}},
        {"in": {"s": "abcdbca"}},
        {"in": {"s": "aguokepatgbnvfqmgmlcupuufxoohdfpgjdmysgvhmvffcnqxjjxqncffvmhvgsymdjgpfdhooxfuupuculmgmqfvnbgtapekouga"}},
        {"in": {"s": stress_true}},
        {"in": {"s": stress_false}},
    ]
