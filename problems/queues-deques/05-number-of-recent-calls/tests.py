import random


def make_test(timestamps):
    return {
        "in": {
            "ops": ["RecentCounter"] + ["ping"] * len(timestamps),
            "args": [[]] + [[t] for t in timestamps],
        }
    }


def visible():
    return [
        make_test([1, 100, 3001, 3002]),
        make_test([100, 3100, 3101, 6101]),
    ]


def hidden():
    rng1 = random.Random(933)
    ts_dense = []
    cur = 1
    for _ in range(1500):
        cur += rng1.randint(1, 35)
        ts_dense.append(cur)

    rng2 = random.Random(9330)
    ts_mixed = []
    cur = 10
    for _ in range(1500):
        cur += rng2.choice([1, 5, 50, 500, 3000, 4500])
        ts_mixed.append(cur)

    return [
        make_test([1]),
        make_test([1, 5000, 10000, 1000000000]),
        make_test(list(range(1, 26))),
        make_test([1, 3000, 3001, 3002, 6000, 6001, 6002]),
        make_test([999996999, 999997000, 999999999, 1000000000]),
        make_test([10, 20, 30, 40, 10000, 10001, 10002, 13000, 13001]),
        make_test([1000 * i for i in range(1, 12)]),
        make_test([1 + 3000 * i for i in range(10)]),
        make_test(ts_dense),
        make_test(ts_mixed),
    ]
