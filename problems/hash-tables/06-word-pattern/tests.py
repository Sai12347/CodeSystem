import random


def visible():
    return [
        {"in": {"pattern": "abba", "s": "dog cat cat dog"}},
        {"in": {"pattern": "abba", "s": "dog cat cat fish"}},
        {"in": {"pattern": "abba", "s": "dog dog dog dog"}},
    ]


def hidden():
    rng = random.Random(290)
    letters = "abcdefghijklmnopqrstuvwxyz"
    vocab = [f"w{chr(97 + i)}{chr(97 + (i * 7) % 26)}" for i in range(26)]
    p_max = "".join(rng.choices(letters, k=300))
    s_max_ok = " ".join(vocab[ord(c) - 97] for c in p_max)
    words_bad = s_max_ok.split(" ")
    words_bad[-1] = "zzz"
    s_max_bad = " ".join(words_bad)

    return [
        {"in": {"pattern": "a", "s": "dog"}},
        {"in": {"pattern": "aaaa", "s": "dog cat cat dog"}},
        {"in": {"pattern": "aaa", "s": "aa aa aa aa"}},
        {"in": {"pattern": "aaaa", "s": "aa aa aa"}},
        # Single-letter words colliding with pattern characters (classic single-map bug!)
        {"in": {"pattern": "abc", "s": "b c a"}},
        {"in": {"pattern": "abba", "s": "a b b a"}},
        {"in": {"pattern": "abc", "s": "a a c"}},
        {"in": {"pattern": "jquery", "s": "jquery"}},
        {"in": {"pattern": "deadbeef", "s": "d e a d b e e f"}},
        {"in": {"pattern": "abacaba", "s": "cat dog cat bird cat dog cat"}},
        {"in": {"pattern": p_max, "s": s_max_ok}},
        {"in": {"pattern": p_max, "s": s_max_bad}},
    ]
