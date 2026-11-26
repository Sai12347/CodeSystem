import random


def visible():
    return [
        {"in": {"s": "barfoothefoobarman", "words": ["foo", "bar"]}},
        {"in": {"s": "wordgoodgoodgoodbestword", "words": ["word", "good", "best", "word"]}},
        {"in": {"s": "barfoofoobarthefoobarman", "words": ["bar", "foo", "the"]}},
    ]


def hidden():
    rng = random.Random(30)
    vocab = ["".join(rng.choice("abcd") for _ in range(4)) for _ in range(12)]
    stress_words = [rng.choice(vocab) for _ in range(25)]
    parts = []
    for block in range(40):
        if block in (5, 17, 31):
            perm = list(stress_words)
            rng.shuffle(perm)
            parts.append("".join(perm))
        else:
            parts.append("".join(rng.choice("abcd") for _ in range(rng.randint(15, 35))))
    stress_s = "".join(parts)

    return [
        {"in": {"s": "a", "words": ["a"]}},
        {"in": {"s": "ab", "words": ["ab", "cd"]}},
        {"in": {"s": "lingmindraboofooowingdingbarrwingmonkeypoundcake", "words": ["fooo", "barr", "wing", "ding", "wing"]}},
        {"in": {"s": "aaaaaaaaaaaaaa", "words": ["aa", "aa"]}},
        {"in": {"s": "abababab", "words": ["a", "b", "a"]}},
        {"in": {"s": "xyzabcdef", "words": ["def", "abc"]}},
        {"in": {"s": "wordgoodgoodgoodbestword", "words": ["word", "good", "best", "good"]}},
        {"in": {"s": "abbabaab", "words": ["ab", "ba"]}},
        {"in": {"s": "zzzzzzzzzz", "words": ["abc", "def"]}},
        {"in": {"s": stress_s, "words": stress_words}},
        {"in": {"s": "abc" * 1000, "words": ["abc"] * 100}},
    ]
