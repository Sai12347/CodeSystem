import random


def visible():
    return [
        {"in": {"s": "ab-cd"}},
        {"in": {"s": "a-bC-dEf-ghIj"}},
        {"in": {"s": "Test1ng-Leet=code-Q!"}},
    ]


def hidden():
    rng = random.Random(917)
    valid_chars = [chr(c) for c in range(33, 123) if chr(c) not in ('"', '\\')]
    letters = [chr(c) for c in range(ord('a'), ord('z') + 1)] + [chr(c) for c in range(ord('A'), ord('Z') + 1)]

    max_mixed = "".join(rng.choice(valid_chars) for _ in range(100))
    max_letters = "".join(rng.choice(letters) for _ in range(100))

    return [
        {"in": {"s": "a"}},
        {"in": {"s": "-"}},
        {"in": {"s": "!@#123-_=+"}},
        {"in": {"s": "abcdefg"}},
        {"in": {"s": "a-b-a"}},
        {"in": {"s": "---AbCd---"}},
        {"in": {"s": "123a456"}},
        {"in": {"s": "a1b2c3d4e5"}},
        {"in": {"s": max_mixed}},
        {"in": {"s": max_letters}},
    ]
