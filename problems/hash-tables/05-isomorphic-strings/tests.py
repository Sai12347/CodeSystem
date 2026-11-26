import random


def visible():
    return [
        {"in": {"s": "egg", "t": "add"}},
        {"in": {"s": "foo", "t": "bar"}},
        {"in": {"s": "paper", "t": "title"}},
    ]


def hidden():
    rng = random.Random(205)
    printable = [chr(c) for c in range(33, 127)]
    perm = list(printable)
    rng.shuffle(perm)
    mapping = dict(zip(printable, perm))

    # Stress 1: true isomorphic string of length 4000 across full printable ASCII
    s_iso = "".join(rng.choices(printable, k=4000))
    t_iso = "".join(mapping[c] for c in s_iso)

    # Stress 2: breaks only at the very last character
    s_late = s_iso
    bad_ch = next(c for c in printable if c != t_iso[-1])
    t_late = t_iso[:-1] + bad_ch

    return [
        {"in": {"s": "a", "t": "b"}},
        {"in": {"s": "a", "t": "a"}},
        {"in": {"s": "badc", "t": "baba"}},
        {"in": {"s": "baba", "t": "badc"}},
        {"in": {"s": "aaaa", "t": "bbbb"}},
        {"in": {"s": "ab", "t": "aa"}},
        {"in": {"s": "A a!1", "t": "B b@2"}},
        {"in": {"s": "Aa", "t": "aa"}},
        {"in": {"s": "13", "t": "42"}},
        {"in": {"s": "bbbaaaba", "t": "aaabbbba"}},
        {"in": {"s": s_iso, "t": t_iso}},
        {"in": {"s": s_late, "t": t_late}},
    ]
