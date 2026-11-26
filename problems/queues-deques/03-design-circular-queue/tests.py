import random


def visible():
    return [
        {"in": {
            "ops": ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"],
            "args": [[3], [1], [2], [3], [4], [], [], [], [4], []]
        }},
        {"in": {
            "ops": ["MyCircularQueue", "isEmpty", "isFull", "Front", "Rear", "deQueue", "enQueue", "Front", "Rear", "isFull"],
            "args": [[1], [], [], [], [], [], [7], [], [], []]
        }},
    ]


def hidden():
    def gen_random(seed, k, n_ops):
        rng = random.Random(seed)
        ops, args = ["MyCircularQueue"], [[k]]
        methods = ["enQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull"]
        weights = [0.35, 0.30, 0.12, 0.12, 0.055, 0.055]
        for _ in range(n_ops):
            m = rng.choices(methods, weights=weights, k=1)[0]
            ops.append(m)
            args.append([rng.randint(0, 1000)] if m == "enQueue" else [])
        return {"in": {"ops": ops, "args": args}}

    # Wrap-around stress for k = 4
    ops_wrap, args_wrap = ["MyCircularQueue"], [[4]]
    for i in range(4):
        ops_wrap.append("enQueue")
        args_wrap.append([i])
    for step in range(25):
        ops_wrap.extend(["deQueue", "Front", "enQueue", "Rear", "isFull"])
        args_wrap.extend([[], [], [step + 10], [], []])

    # Max capacity k = 1000 fill & drain
    ops_max, args_max = ["MyCircularQueue"], [[1000]]
    for i in range(1000):
        ops_max.append("enQueue")
        args_max.append([i % 1001])
    ops_max.extend(["isFull", "enQueue", "Front", "Rear"])
    args_max.extend([[], [999], [], []])
    for _ in range(1000):
        ops_max.append("deQueue")
        args_max.append([])
    ops_max.extend(["isEmpty", "deQueue", "Front", "Rear"])
    args_max.extend([[], [], [], []])

    return [
        {"in": {
            "ops": ["MyCircularQueue", "enQueue", "enQueue", "Front", "Rear", "deQueue", "deQueue", "isEmpty", "enQueue", "Front", "Rear"],
            "args": [[1], [0], [1], [], [], [], [], [], [1000], [], []]
        }},
        {"in": {
            "ops": ["MyCircularQueue", "Front", "Rear", "deQueue", "deQueue", "isEmpty", "isFull"],
            "args": [[5], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularQueue", "enQueue", "enQueue", "Front", "Rear", "deQueue", "Front", "Rear", "deQueue", "Front", "Rear"],
            "args": [[2], [0], [0], [], [], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Front", "Rear", "deQueue", "deQueue", "deQueue", "deQueue", "Front", "Rear"],
            "args": [[2], [5], [5], [5], [5], [5], [], [], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "deQueue", "deQueue", "deQueue", "isEmpty", "enQueue", "enQueue", "Front", "Rear"],
            "args": [[3], [10], [20], [30], [], [], [], [], [40], [50], [], []]
        }},
        {"in": {
            "ops": ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "deQueue", "enQueue", "Front", "Rear", "deQueue", "Front", "Rear"],
            "args": [[3], [1000], [0], [500], [250], [], [750], [], [], [], [], []]
        }},
        {"in": {"ops": ops_wrap, "args": args_wrap}},
        {"in": {"ops": ops_max, "args": args_max}},
        gen_random(622, 7, 1200),
        gen_random(6220, 80, 1500),
    ]
