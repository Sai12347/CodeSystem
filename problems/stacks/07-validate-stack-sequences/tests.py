import random


def visible():
    return [
        {"in": {"pushed": [1, 2, 3, 4, 5], "popped": [4, 5, 3, 2, 1]}},
        {"in": {"pushed": [1, 2, 3, 4, 5], "popped": [4, 3, 5, 1, 2]}},
        {"in": {"pushed": [10], "popped": [10]}},
    ]


def _gen_valid_popped(pushed, rng):
    stack = []
    popped = []
    i = 0
    n = len(pushed)
    while i < n or stack:
        if stack and (i == n or rng.random() < 0.5):
            popped.append(stack.pop())
        else:
            stack.append(pushed[i])
            i += 1
    return popped


def hidden():
    tests = []

    # 1. Minimum length with 0 boundary value
    tests.append({"in": {"pushed": [0], "popped": [0]}})

    # 2. Length 2 - both permutations are always valid
    tests.append({"in": {"pushed": [0, 1000], "popped": [0, 1000]}})
    tests.append({"in": {"pushed": [0, 1000], "popped": [1000, 0]}})

    # 3. Minimal invalid case (3-1-2 pattern)
    tests.append({"in": {"pushed": [1, 2, 3], "popped": [3, 1, 2]}})

    # 4. All other valid length-3 patterns (interleaved)
    tests.append({"in": {"pushed": [2, 1, 0], "popped": [1, 2, 0]}})

    # 5. Identical push and pop order (immediate pop after every push)
    tests.append({"in": {"pushed": list(range(1, 21)), "popped": list(range(1, 21))}})

    # 6. Exact reverse order (push all, then pop all)
    tests.append({"in": {"pushed": list(range(1, 21)), "popped": list(range(20, 0, -1))}})

    # 7. Almost valid - single swap at the very end breaks LIFO
    tests.append({
        "in": {
            "pushed": [1, 2, 3, 4, 5, 6, 7, 8],
            "popped": [2, 1, 4, 3, 6, 5, 8, 7],
        }
    })
    tests.append({
        "in": {
            "pushed": [1, 2, 3, 4, 5, 6, 7, 8],
            "popped": [5, 4, 6, 3, 7, 2, 1, 8],
        }
    })
    tests.append({
        "in": {
            "pushed": [1, 2, 3, 4, 5, 6, 7, 8],
            "popped": [5, 4, 6, 3, 7, 1, 2, 8],
        }
    })

    # 8. Stress test: n = 1000 valid random stack sequence
    rng1 = random.Random(94601)
    pushed1 = list(range(1000))
    rng1.shuffle(pushed1)
    popped1 = _gen_valid_popped(pushed1, rng1)
    tests.append({"in": {"pushed": pushed1, "popped": popped1}})

    # 9. Stress test: n = 1000 invalid (reverse order with last two swapped -> impossible 3-1-2)
    rng2 = random.Random(94602)
    pushed3 = list(range(1, 1001))
    rng2.shuffle(pushed3)
    popped3 = list(reversed(pushed3))
    popped3[-1], popped3[-2] = popped3[-2], popped3[-1]
    tests.append({"in": {"pushed": pushed3, "popped": popped3}})

    return tests
