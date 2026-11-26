import random


def visible():
    return [
        {
            "in": {
                "dictionary": ["cat", "bat", "rat"],
                "sentence": "the cattle was rattled by the battery",
            }
        },
        {
            "in": {
                "dictionary": ["a", "b", "c"],
                "sentence": "aadsfasf absbs bbab cadsfafs",
            }
        },
    ]


def hidden():
    tests = []

    # 1. Shortest root wins among nested roots
    tests.append({
        "in": {
            "dictionary": ["a", "aa", "aaa", "aaaa"],
            "sentence": "a aa a aaaa aaa aaa aaa aaaaaa bbb baba ababa",
        }
    })

    # 2. Longer root appears before shorter root in dictionary
    tests.append({
        "in": {
            "dictionary": ["catt", "cat", "batt", "bat", "ratt", "rat"],
            "sentence": "the cattle was rattled by the battery",
        }
    })

    # 3. Single word sentence, no match
    tests.append({
        "in": {
            "dictionary": ["pre", "pro"],
            "sentence": "algorithm",
        }
    })

    # 4. Single word sentence, exact match to root
    tests.append({
        "in": {
            "dictionary": ["algo"],
            "sentence": "algo",
        }
    })

    # 5. Root longer than sentence word must NOT replace
    tests.append({
        "in": {
            "dictionary": ["application", "apples"],
            "sentence": "app apple apples application applications",
        }
    })

    # 6. Duplicate roots in dictionary
    tests.append({
        "in": {
            "dictionary": ["run", "run", "running", "walk", "walk"],
            "sentence": "runner running walked walking jump",
        }
    })

    # 7. No word in sentence matches any root
    tests.append({
        "in": {
            "dictionary": ["xyz", "mno", "pqr"],
            "sentence": "alpha beta gamma delta epsilon",
        }
    })

    # 8. Every word replaced by varying root lengths
    tests.append({
        "in": {
            "dictionary": ["x", "ab", "cde", "fghi"],
            "sentence": "xtreme absolute cdefg fghijkl ab x",
        }
    })

    # 9. Long roots and long words with near-miss boundaries
    base = "abcdefghij" * 7  # len 70
    tests.append({
        "in": {
            "dictionary": [base, base[:69] + "z", base[:35]],
            "sentence": " ".join([
                base + "extra",
                base[:69],
                base[:34],
                base[:35],
                base[:69] + "z" + "tail",
            ]),
        }
    })

    # 10. Stress test: 300 dictionary roots + 600-word sentence
    rng = random.Random(64801)
    alphabet = "abcdefghijkl"
    roots = ["".join(rng.choice(alphabet) for _ in range(rng.randint(2, 10))) for _ in range(300)]
    words = []
    for _ in range(600):
        if rng.random() < 0.6:
            r = rng.choice(roots)
            tail = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
            words.append(r + tail)
        else:
            words.append("".join(rng.choice(alphabet) for _ in range(rng.randint(2, 12))))
    tests.append({
        "in": {
            "dictionary": roots,
            "sentence": " ".join(words),
        }
    })

    return tests
