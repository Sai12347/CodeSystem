import random


def visible():
    return [
        {"in": {"s": "eleetminicoworoep"}},
        {"in": {"s": "leetcodeisgreat"}},
        {"in": {"s": "bcbcbc"}},
    ]


def hidden():
    rng1 = random.Random(13711)
    letters = "abcdefghijklmnopqrstuvwxyz"
    stress1 = "".join(rng1.choice(letters) for _ in range(2000))

    rng2 = random.Random(13712)
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    stress2 = "".join(
        rng2.choice(vowels) if rng2.random() < 0.6 else rng2.choice(consonants)
        for _ in range(3000)
    )

    return [
        {"in": {"s": "z"}},
        {"in": {"s": "a"}},
        {"in": {"s": "aeiou"}},
        {"in": {"s": "aeiouaeiou"}},
        {"in": {"s": "eeeee"}},
        {"in": {"s": "bcdfghjklmnpqrstvwxyz"}},
        {"in": {"s": "abecidofuabecidofu"}},
        {"in": {"s": "a" + "b" * 10 + "e" + "c" * 10 + "i"}},
        {"in": {"s": "uoieaxxxaeiou"}},
        {"in": {"s": stress1}},
        {"in": {"s": stress2}},
    ]
