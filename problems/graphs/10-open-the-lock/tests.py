import random


def _neighbors(code: str):
    res = []
    for i in range(4):
        d = int(code[i])
        for nd in ((d + 1) % 10, (d + 9) % 10):
            res.append(code[:i] + str(nd) + code[i + 1 :])
    return res


def visible():
    return [
        {"in": {"deadends": ["0201", "0101", "0102", "1212", "2002"], "target": "0202"}},
        {"in": {"deadends": ["8888"], "target": "0009"}},
        {"in": {"deadends": _neighbors("8888"), "target": "8888"}},
    ]


def hidden():
    tests = []

    # 1. Target is already "0000" -> 0 turns
    tests.append({"in": {"deadends": ["0001", "9999"], "target": "0000"}})

    # 2. Starting state "0000" is itself a deadend -> -1
    tests.append({"in": {"deadends": ["0000"], "target": "8888"}})

    # 3. All 8 neighbors of "0000" are deadends -> -1
    tests.append({"in": {"deadends": _neighbors("0000"), "target": "1234"}})

    # 4. Optimal wrap-around on all 4 wheels ("0000" -> "9999" in 4 turns)
    tests.append({"in": {"deadends": ["1000", "0100", "0010", "0001"], "target": "9999"}})

    # 5. Antipodal state "5555" with no blocking deadends (max possible unobstructed distance = 20)
    tests.append({"in": {"deadends": ["1234"], "target": "5555"}})

    # 6. Duplicate deadends in input list
    tests.append({"in": {"deadends": ["0001", "0001", "0010", "0010", "0100", "1000"], "target": "0002"}})

    # 7. Forced detour: only "0009" is an available first move; reach "0002" in 8 turns.
    n7 = [s for s in _neighbors("0000") if s != "0009"]
    tests.append({"in": {"deadends": n7, "target": "0002"}})

    # 8. Target surrounded on 7 sides with a single narrow entrance
    n8 = [s for s in _neighbors("3456") if s != "3457"]
    tests.append({"in": {"deadends": n8 + ["3467", "3447", "3557", "3357"], "target": "3456"}})

    # 9. Stress test: 500 random deadends (max constraint), target "5678" reachable
    rng1 = random.Random(7521)
    dead9 = set()
    while len(dead9) < 500:
        code = f"{rng1.randint(0, 9999):04d}"
        if code not in ("0000", "5678"):
            dead9.add(code)
    tests.append({"in": {"deadends": sorted(dead9), "target": "5678"}})

    # 10. Stress test: 500 deadends including complete cage around target "4729" -> -1
    rng2 = random.Random(7522)
    dead10 = set(_neighbors("4729"))
    while len(dead10) < 500:
        code = f"{rng2.randint(0, 9999):04d}"
        if code not in ("0000", "4729"):
            dead10.add(code)
    dlist10 = list(dead10)
    rng2.shuffle(dlist10)
    tests.append({"in": {"deadends": dlist10, "target": "4729"}})

    return tests
