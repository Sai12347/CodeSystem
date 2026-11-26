import itertools
import random


def _swap(s: str, i: int, j: int) -> str:
    arr = list(s)
    arr[i], arr[j] = arr[j], arr[i]
    return "".join(arr)


def _gen_anagram_clusters(n: int, length: int, num_seeds: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    base = [chr(97 + (i % 10)) for i in range(length)]
    seeds = []
    for _ in range(num_seeds):
        cur = base[:]
        rng.shuffle(cur)
        seeds.append("".join(cur))
    strs = []
    for i in range(n):
        s = seeds[i % num_seeds]
        steps = rng.randint(0, 2)
        for _ in range(steps):
            a = rng.randrange(length)
            b = rng.randrange(length)
            s = _swap(s, a, b)
        strs.append(s)
    rng.shuffle(strs)
    return strs


def visible():
    return [
        {"in": {"strs": ["tars", "rats", "arts", "star"]}},
        {"in": {"strs": ["omv", "ovm"]}},
    ]


def hidden():
    # 1. Single string
    t1 = ["abc"]
    # 2. Single-character strings
    t2 = ["a", "a", "a", "a"]
    # 3. All identical multi-char strings
    t3 = ["abab", "abab", "abab", "abab"]
    # 4. Transitive chain where first and last differ at every position
    t4 = ["abcd", "bacd", "bcad", "bcda"]
    # 5. All 24 permutations of "abcd" (connected by transpositions -> 1 group)
    t5 = ["".join(p) for p in itertools.permutations("abcd")]
    # 6. Completely disjoint strings (every pair at Hamming distance >= 4)
    t6 = ["abcdef", "badcfe", "efcdab", "fedcba"]
    # 7. Bridge string appearing last that merges 2 separate clusters
    t7 = ["abcde", "bacde", "bcdea", "cbdea", "bcade", "bcdae"]
    # 8. Long strings (L = 100) forming 3 distinct clusters
    base = "".join(chr(97 + (i % 26)) for i in range(100))
    c1 = [base, _swap(base, 0, 50), _swap(_swap(base, 0, 50), 10, 90)]
    b2 = base[::-1]
    c2 = [b2, _swap(b2, 1, 2), _swap(b2, 3, 4)]
    b3 = base[50:] + base[:50]
    c3 = [b3, _swap(b3, 0, 99)]
    t8 = c1 + c2 + c3
    # 9. Medium random anagram clusters (n = 80, L = 30)
    t9 = _gen_anagram_clusters(80, 30, 8, 8391)
    # 10. Stress test (n = 250, L = 50)
    t10 = _gen_anagram_clusters(250, 50, 12, 8392)

    return [{"in": {"strs": t}} for t in (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)]
