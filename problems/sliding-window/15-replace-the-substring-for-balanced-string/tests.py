import random


def visible():
    return [
        {"in": {"s": "QWER"}},
        {"in": {"s": "QQWE"}},
        {"in": {"s": "QQQW"}},
    ]


def hidden():
    rng1 = random.Random(1234)
    big_uniform = "".join(rng1.choice("QWER") for _ in range(1200))

    rng2 = random.Random(12340)
    skewed_chars = []
    for _ in range(1200):
        r = rng2.random()
        if r < 0.60:
            skewed_chars.append("Q")
        elif r < 0.80:
            skewed_chars.append("W")
        elif r < 0.90:
            skewed_chars.append("E")
        else:
            skewed_chars.append("R")
    big_skewed = "".join(skewed_chars)

    return [
        {"in": {"s": "QQQQ"}},
        {"in": {"s": "QWERREWQQWER"}},
        {"in": {"s": "WWQQRRRRQRQQ"}},
        {"in": {"s": "WWWWWWWWWWWW"}},
        {"in": {"s": "QWQWQWQW"}},
        {"in": {"s": "QQQWWWEEEQQW"}},
        {"in": {"s": "QWERQQQQQWER"}},
        {"in": {"s": "WWEQERQWQWWRWWERQWEQ"}},
        {"in": {"s": big_uniform}},
        {"in": {"s": big_skewed}},
    ]
