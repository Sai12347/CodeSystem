import random


def _make(prices):
    return {
        "in": {
            "ops": ["StockSpanner"] + ["next"] * len(prices),
            "args": [[]] + [[p] for p in prices],
        }
    }


def visible():
    return [
        _make([100, 80, 60, 70, 60, 75, 85]),
        _make([10, 20, 30, 40]),
    ]


def hidden():
    rng = random.Random(901)
    stress_rand = [rng.randint(1, 100000) for _ in range(1500)]
    stress_wave = [100000 - i for i in range(500)] + [100000] + [i + 1 for i in range(500)]
    return [
        _make([50]),
        _make([100, 100, 100, 100, 100]),
        _make([100, 90, 80, 70, 60, 50]),
        _make([50, 40, 30, 40, 50, 60]),
        _make([1, 100000, 1, 100000, 1]),
        _make([5, 10, 5, 10, 5, 10, 10, 5]),
        _make([28, 14, 28, 35, 46, 53, 66, 80, 87, 88]),
        _make([31, 41, 48, 59, 79, 79, 48, 41, 80]),
        _make(stress_wave),
        _make(stress_rand),
    ]
