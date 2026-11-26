import random


def visible():
    return [
        {"in": {
            "ops": ["MyStack", "push", "push", "top", "pop", "empty"],
            "args": [[], [1], [2], [], [], []]
        }},
        {"in": {
            "ops": ["MyStack", "push", "push", "push", "pop", "pop", "push", "top", "pop", "pop", "empty"],
            "args": [[], [10], [20], [30], [], [], [40], [], [], [], []]
        }},
    ]


def hidden():
    rng = random.Random(225)
    ops_big, args_big = ["MyStack"], [[]]
    size = 0
    for _ in range(700):
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
            if r < 0.5:
                ops_big.append("push")
                args_big.append([rng.randint(-100000, 100000)])
                size += 1
            elif r < 0.78:
                ops_big.append("pop")
                args_big.append([])
                size -= 1
            elif r < 0.92:
                ops_big.append("top")
                args_big.append([])
            else:
                ops_big.append("empty")
                args_big.append([])

    ops_alt, args_alt = ["MyStack"], [[]]
    for i in range(40):
        ops_alt.extend(["push", "top", "pop", "empty"])
        args_alt.extend([[i - 20], [], [], []])

    return [
        {"in": {"ops": ["MyStack", "empty"], "args": [[], []]}},
        {"in": {"ops": ["MyStack", "push", "top", "empty", "pop", "empty"], "args": [[], [99], [], [], [], []]}},
        {"in": {
            "ops": ["MyStack", "push", "push", "push", "top", "pop", "pop", "pop", "empty"],
            "args": [[], [-100000], [0], [100000], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyStack", "push", "push", "push", "pop", "top", "pop", "pop", "empty"],
            "args": [[], [5], [5], [5], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyStack", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "pop"],
            "args": [[], [1], [2], [3], [4], [5], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyStack", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "pop"],
            "args": [[], [5], [4], [3], [2], [1], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyStack", "push", "top", "top", "push", "top", "top", "pop", "top", "pop", "empty"],
            "args": [[], [-1], [], [], [-2], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyStack", "push", "pop", "empty", "push", "push", "pop", "pop", "empty", "push", "top"],
            "args": [[], [3], [], [], [4], [5], [], [], [], [6], []]
        }},
        {"in": {"ops": ops_alt, "args": args_alt}},
        {"in": {"ops": ops_big, "args": args_big}},
    ]
