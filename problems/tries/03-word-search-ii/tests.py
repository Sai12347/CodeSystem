import random


def visible():
    return [
        {
            "in": {
                "board": [
                    ["o", "a", "a", "n"],
                    ["e", "t", "a", "e"],
                    ["i", "h", "k", "r"],
                    ["i", "f", "l", "v"],
                ],
                "words": ["oath", "pea", "eat", "rain"],
            }
        },
        {
            "in": {
                "board": [["a", "b"], ["c", "d"]],
                "words": ["abcb"],
            }
        },
    ]


def hidden():
    tests = []

    # 1. 1x1 board
    tests.append({
        "in": {
            "board": [["a"]],
            "words": ["a", "aa", "b"],
        }
    })

    # 2. Single row board (both directions)
    tests.append({
        "in": {
            "board": [["a", "b", "c", "d", "e"]],
            "words": ["abc", "edc", "bcd", "aba", "ace", "abcde"],
        }
    })

    # 3. Single column board (both directions)
    tests.append({
        "in": {
            "board": [["p"], ["q"], ["r"], ["s"]],
            "words": ["pqrs", "srqp", "qr", "pqs", "qpq"],
        }
    })

    # 4. Cell reuse prevention
    tests.append({
        "in": {
            "board": [
                ["a", "b"],
                ["b", "a"],
            ],
            "words": ["aba", "ababa", "abab", "aa", "bb", "ab", "ba"],
        }
    })

    # 5. Nested prefixes (must continue DFS after finding shorter word)
    tests.append({
        "in": {
            "board": [
                ["a", "b", "c"],
                ["f", "e", "d"],
                ["g", "h", "i"],
            ],
            "words": ["a", "ab", "abc", "abcd", "abcde", "abcdef", "abcdefg", "abcdefgh", "abcdefghi", "abcf"],
        }
    })

    # 6. All-identical board (no duplicates in output, length > cells impossible)
    tests.append({
        "in": {
            "board": [
                ["a", "a", "a"],
                ["a", "a", "a"],
                ["a", "a", "a"],
            ],
            "words": ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaaaaa", "aaaaaaaaaa"],
        }
    })

    # 7. Winding length-10 path on 4x4 board
    tests.append({
        "in": {
            "board": [
                ["s", "t", "a", "r"],
                ["x", "y", "z", "t"],
                ["w", "v", "u", "e"],
                ["m", "n", "o", "d"],
            ],
            "words": ["startedu", "starteduv", "starteduvw", "start", "styx", "dome", "mode", "nomw"],
        }
    })

    # 8. No words found on 5x5 board with near-misses
    tests.append({
        "in": {
            "board": [
                ["a", "b", "c", "d", "e"],
                ["f", "g", "h", "i", "j"],
                ["k", "l", "m", "n", "o"],
                ["p", "q", "r", "s", "t"],
                ["u", "v", "w", "x", "y"],
            ],
            "words": ["abcz", "fghiz", "klmnoq", "z", "agmsy", "aei"],
        }
    })

    # 9. Deterministic 8x8 board with 100 words
    rng = random.Random(21201)
    board9 = [[rng.choice("abcdefghijkl") for _ in range(8)] for _ in range(8)]
    words9 = set()
    # Plant 40 guaranteed paths
    for _ in range(40):
        r, c = rng.randrange(8), rng.randrange(8)
        visited = {(r, c)}
        chars = [board9[r][c]]
        target_len = rng.randint(2, 8)
        for _ in range(target_len - 1):
            nbrs = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= r + dr < 8 and 0 <= c + dc < 8 and (r + dr, c + dc) not in visited]
            if not nbrs:
                break
            r, c = rng.choice(nbrs)
            visited.add((r, c))
            chars.append(board9[r][c])
        words9.add("".join(chars))
    # Add random distractors
    while len(words9) < 100:
        words9.add("".join(rng.choice("abcdefghijkl") for _ in range(rng.randint(2, 8))))
    tests.append({"in": {"board": board9, "words": sorted(words9)}})

    # 10. Stress test: 12x12 max board with 300 words
    rng = random.Random(21202)
    board10 = [[rng.choice("abcdefghijklmnop") for _ in range(12)] for _ in range(12)]
    words10 = set()
    for _ in range(100):
        r, c = rng.randrange(12), rng.randrange(12)
        visited = {(r, c)}
        chars = [board10[r][c]]
        target_len = rng.randint(2, 10)
        for _ in range(target_len - 1):
            nbrs = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= r + dr < 12 and 0 <= c + dc < 12 and (r + dr, c + dc) not in visited]
            if not nbrs:
                break
            r, c = rng.choice(nbrs)
            visited.add((r, c))
            chars.append(board10[r][c])
        words10.add("".join(chars))
    while len(words10) < 300:
        words10.add("".join(rng.choice("abcdefghijklmnop") for _ in range(rng.randint(3, 10))))
    tests.append({"in": {"board": board10, "words": sorted(words10)}})

    return tests
