import random


def _rand_num(rng: random.Random, length: int) -> str:
    first = rng.choice("123456789")
    rest = "".join(rng.choice("0123456789") for _ in range(length - 1))
    return first + rest


def visible():
    return [
        {"in": {"num1": "2", "num2": "3"}},
        {"in": {"num1": "123", "num2": "456"}},
        {"in": {"num1": "0", "num2": "99999"}},
    ]


def hidden():
    rng = random.Random(43)
    return [
        {"in": {"num1": "0", "num2": "0"}},
        {"in": {"num1": "1", "num2": "1"}},
        {"in": {"num1": "9", "num2": "9"}},
        {"in": {"num1": "1", "num2": "98765432109876543210"}},
        {"in": {"num1": "99999999999999999999", "num2": "0"}},
        {"in": {"num1": "999", "num2": "999"}},
        {"in": {"num1": "10000000000", "num2": "10000000000"}},
        {"in": {"num1": "123456789", "num2": "987654321"}},
        {"in": {"num1": "99999999999999999999", "num2": "99999999999999999999"}},
        {"in": {"num1": _rand_num(rng, 200), "num2": _rand_num(rng, 200)}},
        {"in": {"num1": "9" * 200, "num2": "9" * 200}},
    ]
