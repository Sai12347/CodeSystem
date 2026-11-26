import random


def _make_large_palindrome(half_len: int, seed: int, corrupt_mid: bool = False) -> str:
    rng = random.Random(seed)
    alnum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    punct = " ,.:;!?-_()[]{}/@#$%"
    left_alnum = [rng.choice(alnum) for _ in range(half_len)]
    right_alnum = [
        (c.swapcase() if c.isalpha() and rng.random() < 0.5 else c)
        for c in reversed(left_alnum)
    ]
    if corrupt_mid:
        # Ensure the middle pair genuinely disagrees after lowercasing
        c = right_alnum[0].lower()
        right_alnum[0] = "z" if c != "z" else "a"

    def interleave(chars):
        out = []
        for ch in chars:
            if rng.random() < 0.25:
                out.append(rng.choice(punct))
            out.append(ch)
        return "".join(out)

    return interleave(left_alnum) + rng.choice(punct) + interleave(right_alnum)


def visible():
    return [
        {"in": {"s": "A man, a plan, a canal: Panama"}},
        {"in": {"s": "race a car"}},
        {"in": {"s": " "}},
    ]


def hidden():
    return [
        {"in": {"s": "a"}},
        {"in": {"s": "!"}},
        {"in": {"s": ".,;:!?@#$%^&*()_-+=[]{}|"}},
        {"in": {"s": "0P"}},
        {"in": {"s": "12321"}},
        {"in": {"s": "1a2"}},
        {"in": {"s": "Ab, bA"}},
        {"in": {"s": "abccda"}},
        {"in": {"s": "No 'x' in Nixon"}},
        {"in": {"s": _make_large_palindrome(3500, seed=125, corrupt_mid=False)}},
        {"in": {"s": _make_large_palindrome(3500, seed=126, corrupt_mid=True)}},
    ]
