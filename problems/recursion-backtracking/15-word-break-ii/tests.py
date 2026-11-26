import random


def visible():
    return [
        {"in": {"s": "catsanddog", "wordDict": ["cat", "cats", "and", "sand", "dog"]}},
        {"in": {"s": "pineapplepenapple", "wordDict": ["apple", "pen", "applepen", "pine", "pineapple"]}},
        {"in": {"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}},
    ]


def hidden():
    rng = random.Random(42)
    alpha = "abcdefghijklmnopqrstuvwxyz"
    large_dict_set = {"algo", "play", "code", "system", "algoplay", "codes", "ystem", "sys", "tem"}
    while len(large_dict_set) < 300:
        w = "".join(rng.choice(alpha) for _ in range(rng.randint(3, 8)))
        large_dict_set.add(w)
    large_dict = sorted(large_dict_set)

    return [
        # Single character match
        {"in": {"s": "a", "wordDict": ["a"]}},
        # Single character mismatch
        {"in": {"s": "a", "wordDict": ["b"]}},
        # Repeated reuse of words
        {"in": {"s": "aaaa", "wordDict": ["a", "aa", "aaa"]}},
        # Dictionary with noise words and multiple decompositions
        {"in": {"s": "leetcode", "wordDict": ["leet", "code", "le", "et", "co", "de", "xyz"]}},
        # Whole string is itself a word alongside splits
        {"in": {"s": "applepie", "wordDict": ["apple", "pie", "applepie", "app", "le"]}},
        # Matching prefix and suffix but no full tiling
        {"in": {"s": "abcb", "wordDict": ["a", "ab", "bc", "cd"]}},
        # Overlapping prefixes
        {"in": {"s": "goalspecial", "wordDict": ["go", "goal", "goals", "special"]}},
        # Large dictionary stress test (300 unique words, len(s) = 18)
        {"in": {"s": "algoplaycodesystem", "wordDict": large_dict}},
        # Positive memoization stress test (len(s) = 20)
        {"in": {"s": "abababababababababab", "wordDict": ["ab", "abab", "ababab", "abababab"]}},
        # Classic dead-end memoization trap (len(s) = 20, fails only at last char)
        {"in": {"s": "aaaaaaaaaaaaaaaaaaab", "wordDict": ["a", "aa", "aaa", "aaaa", "aaaaa"]}},
    ]
