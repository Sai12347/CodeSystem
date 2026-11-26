import random


def visible():
    return [
        {"in": {
            "ops": ["MyQueue", "push", "push", "peek", "pop", "empty"],
            "args": [[], [1], [2], [], [], []]
        }},
        {"in": {
            "ops": ["MyQueue", "push", "pop", "empty", "push", "push", "peek", "pop", "pop", "empty"],
            "args": [[], [10], [], [], [20], [30], [], [], [], []]
        }},
    ]


def hidden():
    rng = random.Random(232)
    ops_big, args_big = ["MyQueue"], [[]]
    size = 0
    for _ in range(1500):
        r = rng.random()
        if size == 0:
            if r < 0.8:
                ops_big.append("push")
                args_big.append([rng.randint(-100000, 100000)])
                size += 1
            else:
                ops_big.append("empty")
                args_big.append([])
        else:
            if r < 0.48:
                ops_big.append("push")
                args_big.append([rng.randint(-100000, 100000)])
                size += 1
            elif r < 0.78:
                ops_big.append("pop")
                args_big.append([])
                size -= 1
            elif r < 0.92:
                ops_big.append("peek")
                args_big.append([])
            else:
                ops_big.append("empty")
                args_big.append([])

    # Burst push then full drain twice
    ops_burst, args_burst = ["MyQueue"], [[]]
    for cycle in range(2):
        for v in range(cycle * 50, cycle * 50 + 50):
            ops_burst.append("push")
            args_burst.append([v])
        for _ in range(50):
            ops_burst.append("pop")
            args_burst.append([])
        ops_burst.append("empty")
        args_burst.append([])

    return [
        {"in": {"ops": ["MyQueue", "empty"], "args": [[], []]}},
        {"in": {"ops": ["MyQueue", "push", "peek", "empty", "pop", "empty"], "args": [[], [42], [], [], [], []]}},
        {"in": {
            "ops": ["MyQueue", "push", "push", "push", "pop", "push", "push", "peek", "pop", "pop", "pop", "pop", "empty"],
            "args": [[], [1], [2], [3], [], [4], [5], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyQueue", "push", "push", "push", "peek", "pop", "pop", "pop", "empty"],
            "args": [[], [-100000], [0], [100000], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyQueue", "push", "push", "push", "push", "pop", "peek", "pop", "pop", "pop", "empty"],
            "args": [[], [7], [7], [7], [7], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyQueue", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "pop"],
            "args": [[], [1], [2], [3], [4], [5], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyQueue", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "pop"],
            "args": [[], [5], [4], [3], [2], [1], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyQueue", "push", "peek", "peek", "peek", "push", "peek", "pop", "peek", "pop", "empty"],
            "args": [[], [-5], [], [], [], [9], [], [], [], [], []]
        }},
        {"in": {"ops": ops_burst, "args": args_burst}},
        {"in": {"ops": ops_big, "args": args_big}},
    ]
