import random


def make_test(events):
    return {
        "in": {
            "ops": ["Logger"] + ["shouldPrintMessage"] * len(events),
            "args": [[]] + [[ts, msg] for ts, msg in events],
        }
    }


def visible():
    return [
        make_test([(1, "foo"), (2, "bar"), (3, "foo"), (8, "bar"), (10, "foo"), (11, "foo")]),
        make_test([(0, "init"), (9, "init"), (10, "init"), (19, "init"), (20, "init")]),
    ]


def hidden():
    rng1 = random.Random(359)
    msgs1 = [f"msg_{i}" for i in range(25)]
    ev1 = []
    t = 0
    for _ in range(1200):
        t += rng1.choice([0, 0, 1, 1, 2])
        ev1.append((t, rng1.choice(msgs1)))

    rng2 = random.Random(3590)
    msgs2 = [f"svc_{i}_event" for i in range(200)]
    ev2 = []
    t = 0
    for _ in range(1200):
        t += rng2.choice([0, 1, 2, 5, 12, 20])
        ev2.append((t, rng2.choice(msgs2)))

    long_msg = "a" * 30
    burst_ev = [(1, f"k{i}") for i in range(30)] + [(5, f"k{i}") for i in range(15)] + [(101, f"k{i}") for i in range(30)]

    return [
        make_test([(0, "only")]),
        make_test([(10, "a"), (19, "a"), (20, "a"), (29, "a"), (30, "a")]),
        make_test([(0, "a"), (5, "a"), (8, "a"), (9, "a"), (10, "a"), (15, "a"), (20, "a")]),
        make_test([(5, "a"), (5, "b"), (5, "a"), (5, "c"), (5, "b"), (15, "a"), (15, "b"), (15, "c")]),
        make_test([(999999985, "hi"), (999999994, "hi"), (999999995, "hi"), (1000000000, "hi")]),
        make_test([(0, long_msg), (9, long_msg), (10, long_msg), (10, "x"), (11, "x")]),
        make_test(burst_ev),
        make_test([(0, "a"), (2, "b"), (4, "c"), (6, "a"), (8, "b"), (10, "a"), (12, "b"), (14, "c"), (16, "a")]),
        make_test(ev1),
        make_test(ev2),
    ]
