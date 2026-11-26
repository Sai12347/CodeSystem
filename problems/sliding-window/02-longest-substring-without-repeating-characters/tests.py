import random


def visible():
    return [
        {"in": {"s": "abcabcbb"}},
        {"in": {"s": "bbbbb"}},
        {"in": {"s": "pwwkew"}},
    ]


def hidden():
    rng1 = random.Random(301)
    alphabet1 = "abcdefghijklmnopqrstuvwxyz0123456789"
    stress1 = "".join(rng1.choice(alphabet1) for _ in range(4000))

    rng2 = random.Random(302)
    ascii_chars = [chr(c) for c in range(32, 127)]
    chunks = []
    for _ in range(42):
        rng2.shuffle(ascii_chars)
        chunks.append("".join(ascii_chars))
    stress2 = "".join(chunks)[:4000]

    return [
        {"in": {"s": ""}},
        {"in": {"s": "z"}},
        {"in": {"s": " "}},
        {"in": {"s": "abcdefghij0123456789"}},
        {"in": {"s": "abba"}},
        {"in": {"s": "tmmzuxt"}},
        {"in": {"s": "dvdf"}},
        {"in": {"s": "aA!@# aA!@#bB$%"}},
        {"in": {"s": "aaaaabcdefg"}},
        {"in": {"s": stress1}},
        {"in": {"s": stress2}},
    ]
