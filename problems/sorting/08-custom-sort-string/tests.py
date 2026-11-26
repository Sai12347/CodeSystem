import random


def visible():
    return [
        {"in": {"order": "cba", "s": "abcd"}},
        {"in": {"order": "bcafg", "s": "abcd"}},
        {"in": {"order": "kqep", "s": "pekeq"}},
    ]


def hidden():
    rng1 = random.Random(791)
    rng2 = random.Random(792)
    alpha = list("abcdefghijklmnopqrstuvwxyz")
    perm1 = list(alpha)
    rng1.shuffle(perm1)
    stress1_s = "".join(rng1.choice(alpha) for _ in range(200))

    perm2 = list(alpha)
    rng2.shuffle(perm2)
    order2 = "".join(perm2[:13])
    stress2_s = "".join(rng2.choice(alpha) for _ in range(200))

    return [
        {"in": {"order": "a", "s": "a"}},
        {"in": {"order": "xyz", "s": "abcdef"}},
        {"in": {"order": "zyxwvutsrqponmlkjihgfedcba", "s": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"order": "hucw", "s": "utzoampdgkalexslxoqfkdjoczajxtuhqyxvlfatmptqdsochtdzgypsfkgqwbgqbcamdqnqagq"}},
        {"in": {"order": "exv", "s": "xwvee"}},
        {"in": {"order": "abcdef", "s": "zzzzzz"}},
        {"in": {"order": "ba", "s": "ababababab"}},
        {"in": {"order": "z", "s": "abczabcz"}},
        {"in": {"order": "qwertyuiop", "s": "poiuytrewqpoiuytrewq"}},
        {"in": {"order": "".join(perm1), "s": stress1_s}},
        {"in": {"order": order2, "s": stress2_s}},
    ]
