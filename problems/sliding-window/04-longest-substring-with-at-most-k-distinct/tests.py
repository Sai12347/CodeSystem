import random


def visible():
    return [
        {"in": {"s": "eceba", "k": 2}},
        {"in": {"s": "aa", "k": 1}},
        {"in": {"s": "abaccc", "k": 2}},
    ]


def hidden():
    rng1 = random.Random(340)
    alpha15 = "abcdefghijklmno"
    stress1 = "".join(rng1.choice(alpha15) for _ in range(3000))

    rng2 = random.Random(341)
    runs = []
    for _ in range(250):
        ch = rng2.choice("abcdef")
        runs.append(ch * rng2.randint(1, 20))
    stress2 = "".join(runs)[:3000]

    letters52 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return [
        {"in": {"s": "abcde", "k": 0}},
        {"in": {"s": "x", "k": 1}},
        {"in": {"s": "x", "k": 0}},
        {"in": {"s": "abcabc", "k": 10}},
        {"in": {"s": "zzzzzzzz", "k": 3}},
        {"in": {"s": "aAbBcCdD", "k": 2}},
        {"in": {"s": "ababcdcdeeeeeeee", "k": 2}},
        {"in": {"s": "11 22 33 1111", "k": 2}},
        {"in": {"s": letters52 * 2, "k": 50}},
        {"in": {"s": stress1, "k": 5}},
        {"in": {"s": stress2, "k": 1}},
    ]
