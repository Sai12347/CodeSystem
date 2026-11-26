import random


def _all_longest_palindromes(s: str) -> list[str]:
    n = len(s)
    best_len = 0
    best = []
    seen = set()

    def expand(l: int, r: int):
        nonlocal best_len, best, seen
        while l >= 0 and r < n and s[l] == s[r]:
            length = r - l + 1
            if length > best_len:
                best_len = length
                sub = s[l:r + 1]
                best = [sub]
                seen = {sub}
            elif length == best_len:
                sub = s[l:r + 1]
                if sub not in seen:
                    seen.add(sub)
                    best.append(sub)
            l -= 1
            r += 1

    for i in range(n):
        expand(i, i)
        expand(i, i + 1)
    return best


def _case(s: str) -> dict:
    return {"in": {"s": s}, "out": _all_longest_palindromes(s)}


def _stress_planted(seed: int) -> str:
    rng = random.Random(seed)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    base = [rng.choice(alphabet) for _ in range(1000)]
    # Plant two distinct tied 101-char palindromes at indices 120 and 680
    half1 = [rng.choice(alphabet) for _ in range(50)]
    pal1 = half1 + [rng.choice(alphabet)] + half1[::-1]
    half2 = [rng.choice(alphabet) for _ in range(50)]
    pal2 = half2 + [rng.choice(alphabet)] + half2[::-1]
    base[120:221] = pal1
    base[680:781] = pal2
    return "".join(base)


def visible():
    return [
        _case("babad"),
        _case("cbbd"),
        _case("racecar"),
    ]


def hidden():
    return [
        _case("a"),
        _case("ac"),
        _case("aa"),
        _case("zzzzzzzzzz"),
        _case("abcdefg"),
        _case("xyzabba"),
        _case("Abba1221abBA"),
        _case("aacabdkacaa"),
        _case("abacdfgdcaba"),
        _case("a" * 1000),
        _case(_stress_planted(seed=5)),
    ]
