import random


def visible():
    return [
        {"in": {"s": "abcd", "t": "bcdf", "maxCost": 3}},
        {"in": {"s": "abcd", "t": "cdef", "maxCost": 3}},
        {"in": {"s": "abcd", "t": "acde", "maxCost": 0}},
    ]


def hidden():
    rng1 = random.Random(1208)
    alpha = "abcdefghijklmnopqrstuvwxyz"
    s_big = "".join(rng1.choice(alpha) for _ in range(2000))
    t_big = "".join(rng1.choice(alpha) for _ in range(2000))

    rng2 = random.Random(12080)
    s_zero = "".join(rng2.choice("abcd") for _ in range(2500))
    t_zero = "".join(
        s_zero[i] if rng2.random() < 0.7 else rng2.choice("abcd")
        for i in range(2500)
    )

    return [
        {"in": {"s": "a", "t": "a", "maxCost": 0}},
        {"in": {"s": "a", "t": "z", "maxCost": 24}},
        {"in": {"s": "a", "t": "z", "maxCost": 25}},
        {"in": {"s": "leetcode", "t": "leetcode", "maxCost": 0}},
        {"in": {"s": "aaaa", "t": "zzzz", "maxCost": 10}},
        {"in": {"s": "azbycx", "t": "zaybxc", "maxCost": 1000000}},
        {"in": {"s": "abzdefg", "t": "abaefgh", "maxCost": 4}},
        {"in": {"s": "krrgw", "t": "zjxss", "maxCost": 19}},
        {"in": {"s": s_big, "t": t_big, "maxCost": 1500}},
        {"in": {"s": s_zero, "t": t_zero, "maxCost": 0}},
    ]
