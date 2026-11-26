import random


def visible():
    return [
        {"in": {"senate": "RD"}},
        {"in": {"senate": "RDD"}},
        {"in": {"senate": "DDRRR"}},
    ]


def hidden():
    rng1 = random.Random(649)
    s_big1 = "".join(rng1.choice("RD") for _ in range(4000))

    rng2 = random.Random(6490)
    chars = ["R"] * 2500 + ["D"] * 2500
    rng2.shuffle(chars)
    s_big2 = "".join(chars)

    return [
        {"in": {"senate": "R"}},
        {"in": {"senate": "D"}},
        {"in": {"senate": "RRRRR"}},
        {"in": {"senate": "DDDDDD"}},
        {"in": {"senate": "RRDDD"}},
        {"in": {"senate": "DRRDRDRDRDDRDRDR"}},
        {"in": {"senate": "RD" * 25}},
        {"in": {"senate": "DR" * 25}},
        {"in": {"senate": "R" * 50 + "D" * 50}},
        {"in": {"senate": "D" * 50 + "R" * 50}},
        {"in": {"senate": s_big1}},
        {"in": {"senate": s_big2}},
    ]
