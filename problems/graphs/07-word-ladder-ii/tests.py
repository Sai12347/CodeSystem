import random


def visible():
    return [
        {"in": {"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log", "cog"]}},
        {"in": {"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log"]}},
        {"in": {"beginWord": "a", "endWord": "c", "wordList": ["a", "b", "c"]}},
    ]


def hidden():
    tests = []

    # 1. Direct single-step transformation with minimal dictionary size 1
    tests.append({"in": {"beginWord": "cat", "endWord": "bat", "wordList": ["bat"]}})

    # 2. beginWord already present in wordList with multiple shortest paths
    tests.append({"in": {
        "beginWord": "red",
        "endWord": "tax",
        "wordList": ["ted", "tex", "red", "tax", "tad", "den", "rex", "pee"],
    }})

    # 3. Single-character words, unreachable (endWord missing)
    tests.append({"in": {"beginWord": "a", "endWord": "z", "wordList": ["b", "c", "d"]}})

    # 4. Disconnected components where endWord IS in wordList
    tests.append({"in": {
        "beginWord": "cold",
        "endWord": "warm",
        "wordList": ["bold", "bald", "ball", "tall", "worm", "warm", "farm", "form"],
    }})

    # 5. 3D hypercube: all 3! = 6 shortest paths from "aaa" to "bbb"
    tests.append({"in": {
        "beginWord": "aaa",
        "endWord": "bbb",
        "wordList": ["aab", "aba", "baa", "abb", "bab", "bba", "bbb"],
    }})

    # 6. Shortcut vs longer detours: must return only shortest paths
    tests.append({"in": {
        "beginWord": "hot",
        "endWord": "dog",
        "wordList": ["hot", "hog", "dog", "dot", "lot", "log", "cog", "cot"],
    }})

    # 7. Max length L = 5 unique path with dead-end decoys
    tests.append({"in": {
        "beginWord": "abcde",
        "endWord": "zzzzz",
        "wordList": [
            "zbcde", "zzcde", "zzzde", "zzzze", "zzzzz",
            "abcdf", "abcdg", "zbcdf", "zzcdf", "zzzdf",
        ],
    }})

    # 8. Dead-end heavy graph (many dead-end branches from beginWord)
    tests.append({"in": {
        "beginWord": "aaaa",
        "endWord": "zzzz",
        "wordList": [
            "baaa", "caaa", "daaa", "eaaa", "faaa",
            "bbaa", "bcaa", "bdaa", "cbaa", "ccaa",
            "bbba", "bbca", "cbba", "ccba",
            "zaaa", "zzaa", "zzza", "zzzz",
            "aaza", "azza", "azzz",
        ],
    }})

    # 9. Converging multi-diamond chain (2^4 = 16 shortest paths)
    # aaaaa -> {baaaa, caaaa} -> daaaa -> {dbaaa, dcaaa} -> ddaaa -> {ddbaa, ddcaa} -> dddaa -> {dddba, dddca} -> dddda
    tests.append({"in": {
        "beginWord": "aaaaa",
        "endWord": "dddda",
        "wordList": [
            "baaaa", "caaaa", "daaaa",
            "dbaaa", "dcaaa", "ddaaa",
            "ddbaa", "ddcaa", "dddaa",
            "dddba", "dddca", "dddda",
            "eaaaa", "edaaa", "eddaa", "eddda",
        ],
    }})

    # 10. Larger stress test: 480 unique 5-letter words with controlled diamond paths + random distractors
    rng = random.Random(12601)
    # Build a 3-diamond backbone (2^3 = 8 shortest paths) using letters a-d,
    # and fill remaining words from letters m-z so distractors cannot create unintended shortcuts.
    backbone = [
        "aaaaa",
        "baaaa", "caaaa", "daaaa",
        "dbaaa", "dcaaa", "ddaaa",
        "ddbaa", "ddcaa", "dddaa",
    ]
    wset = set(backbone[1:])
    alph = "mnopqrstuvwxyz"
    while len(wset) < 480:
        w = "".join(rng.choice(alph) for _ in range(5))
        wset.add(w)
    wl = list(wset)
    rng.shuffle(wl)
    tests.append({"in": {"beginWord": "aaaaa", "endWord": "dddaa", "wordList": wl}})

    return tests
