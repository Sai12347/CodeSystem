import random


def _rand_words(rng: random.Random, count: int, max_word_len: int):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, max_word_len))) for _ in range(count)]


def visible():
    return [
        {"in": {"words": ["This", "is", "an", "example", "of", "text", "justification."], "maxWidth": 16}},
        {"in": {"words": ["What", "must", "be", "acknowledgment", "shall", "be"], "maxWidth": 16}},
        {"in": {"words": ["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain", "to", "a", "computer.", "Art", "is", "everything", "else", "we", "do"], "maxWidth": 20}},
    ]


def hidden():
    rng1 = random.Random(68)
    rng2 = random.Random(680)
    return [
        {"in": {"words": ["hello"], "maxWidth": 5}},
        {"in": {"words": ["a"], "maxWidth": 10}},
        {"in": {"words": ["a", "b", "c"], "maxWidth": 1}},
        {"in": {"words": ["abcd", "efgh", "ijkl"], "maxWidth": 4}},
        {"in": {"words": ["Listen", "to", "many,", "speak", "to", "a", "few."], "maxWidth": 6}},
        {"in": {"words": ["a", "b", "c", "d", "e"], "maxWidth": 7}},
        {"in": {"words": ["a", "b", "c", "d", "last"], "maxWidth": 8}},
        {"in": {"words": ["The", "quick", "brown", "fox", "jumps"], "maxWidth": 30}},
        {"in": {"words": ["v2.0:", "100%", "fast,", "zero-cost!", "OK?"], "maxWidth": 12}},
        {"in": {"words": _rand_words(rng1, 300, 20), "maxWidth": 50}},
        {"in": {"words": _rand_words(rng2, 300, 15), "maxWidth": 100}},
    ]
