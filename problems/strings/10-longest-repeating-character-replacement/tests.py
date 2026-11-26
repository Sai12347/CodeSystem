import random


def visible():
    return [
        {"in": {"s": "ABAB", "k": 2}},
        {"in": {"s": "AABABBA", "k": 1}},
        {"in": {"s": "ABCDE", "k": 0}},
    ]


def hidden():
    rng1 = random.Random(424)
    rng2 = random.Random(4242)
    stress1 = "".join(rng1.choice("ABCDE") for _ in range(10000))
    stress2 = "".join(rng2.choice("AABBBC") for _ in range(10000))
    return [
        {"in": {"s": "A", "k": 0}},
        {"in": {"s": "Z", "k": 1}},
        {"in": {"s": "AAAAAA", "k": 0}},
        {"in": {"s": "ABCDEFG", "k": 7}},
        {"in": {"s": "AAABBBBBCCDDDD", "k": 0}},
        {"in": {"s": "BAAAB", "k": 2}},
        {"in": {"s": "ABBB", "k": 2}},
        {"in": {"s": "AAABAAA", "k": 1}},
        {"in": {"s": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "k": 5}},
        {"in": {"s": "KRSCDCSONAJNHLBMDQGIFCPEKPOHQIHLTDIQGEKLRLCQNBOHNDQGHJPNDQPERNFSSSRDEQLFPCCCARFMDLHADJADAGNNSBNCJQOF", "k": 4}},
        {"in": {"s": stress1, "k": 50}},
        {"in": {"s": stress2, "k": 500}},
    ]
