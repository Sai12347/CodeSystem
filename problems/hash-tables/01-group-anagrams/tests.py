import random


def visible():
    return [
        {"in": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}},
        {"in": {"strs": [""]}},
        {"in": {"strs": ["a"]}},
    ]


def hidden():
    rng = random.Random(49)
    # Larger stress test: 1500 strings drawn from 60 base words and random permutations
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    bases = ["".join(rng.choices(alphabet, k=rng.randint(4, 15))) for _ in range(60)]
    stress = []
    for _ in range(1500):
        chars = list(rng.choice(bases))
        rng.shuffle(chars)
        stress.append("".join(chars))

    # Max-length strings (length 100) that differ by only 1 letter vs true anagrams
    long_base = "a" * 50 + "b" * 30 + "z" * 20
    long_anagram = "z" * 20 + "a" * 25 + "b" * 30 + "a" * 25
    long_diff = "a" * 49 + "b" * 31 + "z" * 20

    return [
        {"in": {"strs": ["", "", ""]}},
        {"in": {"strs": ["abc", "def", "ghi", "jkl"]}},
        {"in": {"strs": ["listen", "silent", "enlist", "tinsel", "inlets"]}},
        {"in": {"strs": ["eat", "eat", "tea", "ate", "tea"]}},
        {"in": {"strs": ["bdddddddddd", "bbbbbbbbbbc"]}},
        {"in": {"strs": ["a", "aa", "aaa", "aaaa", "a", "aa"]}},
        {"in": {"strs": ["", "a", "", "b", "a", "ab", "ba"]}},
        {"in": {"strs": ["cab", "tin", "pew", "duh", "may", "ill", "buy", "bar", "max", "doc"]}},
        {"in": {"strs": [long_base, long_anagram, long_diff]}},
        {"in": {"strs": stress}},
    ]
