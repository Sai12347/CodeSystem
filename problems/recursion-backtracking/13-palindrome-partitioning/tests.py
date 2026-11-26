def visible():
    return [
        {"in": {"s": "aab"}},
        {"in": {"s": "a"}},
        {"in": {"s": "aba"}},
    ]


def hidden():
    return [
        {"in": {"s": "ab"}},
        {"in": {"s": "aa"}},
        {"in": {"s": "aaa"}},
        {"in": {"s": "abba"}},
        {"in": {"s": "racecar"}},
        {"in": {"s": "aabb"}},
        {"in": {"s": "ababa"}},
        {"in": {"s": "abcdefgh"}},
        {"in": {"s": "aaaaaaaaaa"}},
        {"in": {"s": "abacabadabacaba"}},
        {"in": {"s": "aabbccddeeffgghh"}},
    ]
