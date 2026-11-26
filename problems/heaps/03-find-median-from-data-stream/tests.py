import random


def _build_stream_ops(nums, query_every=1):
    ops = ["MedianFinder"]
    args = [[]]
    for i, x in enumerate(nums, 1):
        ops.append("addNum")
        args.append([x])
        if i % query_every == 0:
            ops.append("findMedian")
            args.append([])
    if ops[-1] != "findMedian":
        ops.append("findMedian")
        args.append([])
    return {"ops": ops, "args": args}


def visible():
    return [
        {"in": {
            "ops": ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
            "args": [[], [1], [2], [], [3], []],
        }},
        {"in": _build_stream_ops([-1, -2, -3, -4, -5], query_every=1)},
    ]


def hidden():
    rng1 = random.Random(29501)
    stress1 = [rng1.randint(-100000, 100000) for _ in range(1200)]

    rng2 = random.Random(29502)
    stress2 = [rng2.choice([-100000, 0, 1, 100000]) for _ in range(1000)]

    return [
        {"in": _build_stream_ops([42], query_every=1)},
        {"in": _build_stream_ops([0, 0, 0, 0, 0], query_every=1)},
        {"in": _build_stream_ops([1, 2, 3, 4, 5, 6, 7, 8], query_every=1)},
        {"in": _build_stream_ops([8, 7, 6, 5, 4, 3, 2, 1], query_every=1)},
        {"in": _build_stream_ops([-100000, 100000, -100000, 100000], query_every=1)},
        {"in": _build_stream_ops([6, 10, 2, 6, 5, 0, 6, 3, 1, 0, 0], query_every=1)},
        {"in": {
            "ops": ["MedianFinder", "addNum", "findMedian", "findMedian", "addNum", "findMedian", "findMedian"],
            "args": [[], [10], [], [], [21], [], []],
        }},
        {"in": _build_stream_ops([100, -100, 50, -50, 25, -25, 0, 1, -1], query_every=1)},
        {"in": _build_stream_ops(stress1, query_every=4)},
        {"in": _build_stream_ops(stress2, query_every=5)},
    ]
