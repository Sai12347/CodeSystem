import random


def _make_stress(seed: int, swap_last: bool):
    rng = random.Random(seed)
    letters = list("abcdefghijklmnopqrstuvwxyz")
    rng.shuffle(letters)
    order = "".join(letters)
    rank = {ch: i for i, ch in enumerate(order)}
    words_set = set()
    while len(words_set) < 100:
        w = "".join(rng.choice(letters) for _ in range(rng.randint(1, 20)))
        words_set.add(w)
    words = sorted(words_set, key=lambda w: [rank[c] for c in w])
    if swap_last:
        words[-1], words[-2] = words[-2], words[-1]
    return {"in": {"words": words, "order": order}}


def visible():
    return [
        {"in": {"words": ["hello", "leetcode"], "order": "hlabcdefgijkmnopqrstuvwxyz"}},
        {"in": {"words": ["word", "world", "row"], "order": "worldabcefghijkmnpqstuvxyz"}},
        {"in": {"words": ["apple", "app"], "order": "abcdefghijklmnopqrstuvwxyz"}},
    ]


def hidden():
    return [
        {"in": {"words": ["alien"], "order": "zyxwvutsrqponmlkjihgfedcba"}},
        {"in": {"words": ["same", "same", "same"], "order": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"words": ["app", "apple", "apples"], "order": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"words": ["z", "y", "x", "a"], "order": "zyxwvutsrqponmlkjihgfedcba"}},
        {"in": {"words": ["a", "b", "c", "e", "d"], "order": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"words": ["aaaaaaaaaaaaaaaaaaab", "aaaaaaaaaaaaaaaaaaac"], "order": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"words": ["aaaaaaaaaaaaaaaaaaac", "aaaaaaaaaaaaaaaaaaab"], "order": "abcdefghijklmnopqrstuvwxyz"}},
        {"in": {"words": ["kuvp", "q"], "order": "ngxlkthsjuoqcpavbfdermiywz"}},
        {"in": {"words": ["a", "aa", "aaa", "aa"], "order": "abcdefghijklmnopqrstuvwxyz"}},
        _make_stress(953, swap_last=False),
        _make_stress(9530, swap_last=True),
    ]
