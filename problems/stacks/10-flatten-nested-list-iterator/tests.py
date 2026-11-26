import random


def visible():
    return [
        {"in": {"nestedList": [[1, 1], 2, [1, 1]]}},
        {"in": {"nestedList": [1, [4, [6]]]}},
        {"in": {"nestedList": [[], [[]], 5, [], [[], 9], []]}},
    ]


def _make_deep(depth, val):
    cur = [val]
    for _ in range(depth - 1):
        cur = [cur]
    return cur


def _gen_nested(rng, budget, max_depth, depth=0):
    res = []
    while budget[0] > 0 and len(res) < 8:
        budget[0] -= 1
        r = rng.random()
        if depth < max_depth and r < 0.30:
            res.append(_gen_nested(rng, budget, max_depth, depth + 1))
        elif depth < max_depth and r < 0.42:
            res.append([])
        else:
            res.append(rng.randint(-1000000, 1000000))
    return res


def hidden():
    tests = []

    # 1. Only a single empty list -> yields []
    tests.append({"in": {"nestedList": [[]]}})

    # 2. Deeply nested empty lists only -> yields []
    tests.append({"in": {"nestedList": [[], [[]], [[[]]], [[], [[]]]]}})

    # 3. Single integer at top level
    tests.append({"in": {"nestedList": [42]}})

    # 4. Flat list with negative, zero, and boundary values (+/- 10^6)
    tests.append({"in": {"nestedList": [-1000000, 0, 1000000, -1, 1]}})

    # 5. Trailing empty nested lists after the last integer
    tests.append({"in": {"nestedList": [1, 2, [], [[]], [[[]]]]}})

    # 6. Leading empty nested lists before the first integer
    tests.append({"in": {"nestedList": [[[[[]]]], [], [[], []], -7]}})

    # 7. Deeply nested single value (depth 80)
    tests.append({"in": {"nestedList": [_make_deep(80, 999)]}})

    # 8. Deeply nested empty chain followed by a value followed by another deep chain
    tests.append({"in": {"nestedList": [_make_deep(50, []), -5, _make_deep(50, 77), _make_deep(40, [])]}})

    # 9. Alternating integers and empty/single-element nested lists
    tests.append({"in": {"nestedList": [1, [], [2], [[]], [[3]], [[[]]], 4, [5, [], [6, []]]]}})

    # 10. Stress test: wide top-level list (length 500) with mixed nested sublists
    rng1 = random.Random(34101)
    wide = []
    for _ in range(500):
        c = rng1.random()
        if c < 0.15:
            wide.append([])
        elif c < 0.45:
            wide.append([rng1.randint(-1000000, 1000000) for _ in range(rng1.randint(0, 5))])
        else:
            wide.append(rng1.randint(-1000000, 1000000))
    tests.append({"in": {"nestedList": wide}})

    # 11. Stress test: random nested tree up to depth 15 with ~1500 nodes
    rng2 = random.Random(34102)
    tree = []
    for _ in range(60):
        budget = [25]
        tree.append(_gen_nested(rng2, budget, max_depth=12))
    tests.append({"in": {"nestedList": tree}})

    return tests
