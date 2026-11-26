import random


def _rand_str(n: int, seed: int) -> str:
    rng = random.Random(seed)
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,."
    return "".join(rng.choice(chars) for _ in range(n))


def visible():
    return [
        {"in": {"s": "PAYPALISHIRING", "numRows": 3}},
        {"in": {"s": "PAYPALISHIRING", "numRows": 4}},
        {"in": {"s": "A", "numRows": 1}},
    ]


def hidden():
    return [
        {"in": {"s": "ABCDEFG", "numRows": 1}},
        {"in": {"s": "ABCDEFGH", "numRows": 2}},
        {"in": {"s": "HELLO", "numRows": 5}},
        {"in": {"s": "AB", "numRows": 10}},
        {"in": {"s": "ABCDE", "numRows": 4}},
        {"in": {"s": "Hello,World.ZigZag,Test.", "numRows": 5}},
        {"in": {"s": "aaaaaaaaaa", "numRows": 4}},
        {"in": {"s": "ABCDEFGHIJKLMNOP", "numRows": 5}},
        {"in": {"s": _rand_str(1000, seed=6), "numRows": 17}},
        {"in": {"s": _rand_str(1000, seed=7), "numRows": 999}},
    ]
