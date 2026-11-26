import random


def visible():
    return [
        {"in": {"s": "ADOBECODEBANC", "t": "ABC"}},
        {"in": {"s": "a", "t": "a"}},
        {"in": {"s": "a", "t": "aa"}},
    ]


def hidden():
    rng1 = random.Random(76)
    noise_alpha = "defghijklmnopqrstuvwxyzDEFGHIJKLMNOPQRSTUVWXYZ"
    # Build a 2500-char string with widely spaced decoy a/b/c and ONE unique minimal window "aXbYcZaa" -> length 8 for t="aaabc"
    parts = []
    for idx in range(50):
        chunk = "".join(rng1.choice(noise_alpha) for _ in range(45))
        if idx == 33:
            parts.append(chunk[:20] + "aXbYcZaa" + chunk[20:])
        else:
            # Put at most one target char separated by >= 15 noise chars so no decoy window can be <= 8
            parts.append(chunk[:15] + "abc"[idx % 3] + chunk[15:])
    stress1 = "".join(parts)

    rng2 = random.Random(77)
    noise_no_z = "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY"
    chars2 = [rng2.choice(noise_no_z) for _ in range(2500)]
    chars2[400] = "Z"
    chars2[1900] = "Z"
    stress2 = "".join(chars2)

    return [
        {"in": {"s": "ab", "t": "abc"}},
        {"in": {"s": "a", "t": "b"}},
        {"in": {"s": "aAbBcCabc", "t": "ABC"}},
        {"in": {"s": "aaflslflsldkalskaaa", "t": "aaa"}},
        {"in": {"s": "cabwefgewcwaefgcf", "t": "cae"}},
        {"in": {"s": "ABCXXXAXBXCXX", "t": "ABC"}},
        {"in": {"s": "XXAXBXCXXXXABC", "t": "ABC"}},
        {"in": {"s": "abacaba", "t": "aaaabbc"}},
        {"in": {"s": "bbaac", "t": "aba"}},
        {"in": {"s": stress1, "t": "aaabc"}},
        {"in": {"s": stress2, "t": "ZZZ"}},
    ]
