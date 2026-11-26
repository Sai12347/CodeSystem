import random


def visible():
    return [
        {"in": {"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log", "cog"]}},
        {"in": {"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log"]}},
        {"in": {"beginWord": "a", "endWord": "c", "wordList": ["a", "b", "c"]}},
    ]


def hidden():
    tests = []

    # 1. Single-character words, unreachable (endWord missing)
    tests.append({"in": {"beginWord": "a", "endWord": "b", "wordList": ["c", "d", "e"]}})

    # 2. Direct single-step transformation with minimal dictionary size 1
    tests.append({"in": {"beginWord": "cat", "endWord": "bat", "wordList": ["bat"]}})

    # 3. beginWord is already in wordList
    tests.append({"in": {
        "beginWord": "red",
        "endWord": "tax",
        "wordList": ["red", "ted", "tex", "tax", "tad", "den", "rex", "pee"],
    }})

    # 4. Multiple paths of different lengths (shortcut vs detour)
    tests.append({"in": {
        "beginWord": "aaaa",
        "endWord": "bbbb",
        "wordList": [
            "baaa", "bbaa", "bbba", "bbbb",
            "aaab", "aabb", "abbb", "abaa", "abba",
            "caaa", "ccaa", "ccca", "cccb", "ccbb", "cbbb",
        ],
    }})

    # 5. Disconnected components where endWord IS in wordList
    tests.append({"in": {
        "beginWord": "cold",
        "endWord": "warm",
        "wordList": ["cord", "card", "ward", "worm", "warm", "bold", "bald"],
    }})

    # 6. Disconnected: truly unreachable even with endWord present
    tests.append({"in": {
        "beginWord": "cold",
        "endWord": "warm",
        "wordList": ["bold", "bald", "ball", "tall", "worm", "warm", "farm", "form"],
    }})

    # 7. Max word length (L = 10) chain
    chain = [
        "abcdefghij",
        "zbcdefghij",
        "zzcdefghij",
        "zzzdefghij",
        "zzzzefghij",
        "zzzzzfghij",
        "zzzzzzghij",
        "zzzzzzzhij",
        "zzzzzzzzij",
        "zzzzzzzzzj",
        "zzzzzzzzzz",
    ]
    tests.append({"in": {
        "beginWord": chain[0],
        "endWord": chain[-1],
        "wordList": chain[1:] + ["abcdefghik", "zbcdefghik", "zzcdefghik"],
    }})

    # 8. Dead-end branches with shared prefixes/suffixes
    tests.append({"in": {
        "beginWord": "sand",
        "endWord": "acne",
        "wordList": [
            "send", "sane", "sine", "line", "lane", "land", "band", "bank",
            "bark", "dark", "dare", "care", "cane", "acne", "acre", "ache",
            "sank", "sink", "link", "lick", "luck",
        ],
    }})

    # 9. Medium random 4-letter graph over small alphabet ('a'..'e')
    rng1 = random.Random(1271)
    alph1 = "abcde"
    pool1 = sorted({"".join(rng1.choice(alph1) for _ in range(4)) for _ in range(420)})
    begin9 = "aaaa"
    end9 = "eeee"
    wset9 = set(pool1)
    wset9.add(end9)
    wset9.discard(begin9)
    tests.append({"in": {"beginWord": begin9, "endWord": end9, "wordList": sorted(wset9)}})

    # 10. Larger stress test: 1000 unique 5-letter words over 'a'..'e' (~8KB JSON)
    rng2 = random.Random(1272)
    alph2 = "abcde"
    wset10 = set()
    begin10 = "aaaaa"
    end10 = "eeeee"
    # Guarantee a valid path exists plus rich random branching
    cur = list(begin10)
    for i in range(5):
        cur[i] = "e"
        wset10.add("".join(cur))
    while len(wset10) < 1000:
        w = "".join(rng2.choice(alph2) for _ in range(5))
        if w != begin10:
            wset10.add(w)
    wl10 = list(wset10)
    rng2.shuffle(wl10)
    tests.append({"in": {"beginWord": begin10, "endWord": end10, "wordList": wl10}})

    return tests
