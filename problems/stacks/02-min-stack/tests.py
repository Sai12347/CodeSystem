import random


def visible():
    return [
        {"in": {
            "ops": ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
            "args": [[], [-2], [0], [-3], [], [], [], []]
        }},
        {"in": {
            "ops": ["MinStack", "push", "push", "getMin", "pop", "getMin"],
            "args": [[], [0], [0], [], [], []]
        }},
    ]


def hidden():
    rng = random.Random(155)
    ops_big, args_big = ["MinStack"], [[]]
    size = 0
    for _ in range(1500):
        if size == 0 or rng.random() < 0.6:
            ops_big.append("push")
            args_big.append([rng.randint(-10**9, 10**9)])
            size += 1
        else:
            choice = rng.choice(["pop", "top", "getMin"])
            ops_big.append(choice)
            args_big.append([])
            if choice == "pop":
                size -= 1

    return [
        {"in": {"ops": ["MinStack", "push", "top", "getMin"], "args": [[], [42], [], []]}},
        {"in": {"ops": ["MinStack", "push", "push", "getMin", "pop", "getMin"], "args": [[], [-2147483648], [2147483647], [], [], []]}},
        {"in": {"ops": ["MinStack", "push", "push", "getMin", "pop", "getMin"], "args": [[], [2147483647], [-2147483648], [], [], []]}},
        {"in": {"ops": ["MinStack", "push", "push", "push", "pop", "getMin", "pop", "getMin"], "args": [[], [3], [2], [1], [], [], [], []]}},
        {"in": {"ops": ["MinStack", "push", "push", "push", "pop", "getMin", "pop", "getMin"], "args": [[], [1], [2], [3], [], [], [], []]}},
        {"in": {"ops": ["MinStack", "push", "pop", "push", "top", "getMin"], "args": [[], [10], [], [-5], [], []]}},
        {"in": {"ops": ["MinStack", "push", "push", "push", "push", "pop", "getMin", "pop", "getMin", "pop", "getMin"], "args": [[], [2], [0], [3], [0], [], [], [], [], [], []]}},
        {"in": {"ops": ops_big, "args": args_big}},
    ]
