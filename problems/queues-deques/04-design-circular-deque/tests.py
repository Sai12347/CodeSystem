import random


def visible():
    return [
        {"in": {
            "ops": ["MyCircularDeque", "insertLast", "insertLast", "insertFront", "insertFront", "getRear", "isFull", "deleteLast", "insertFront", "getFront"],
            "args": [[3], [1], [2], [3], [4], [], [], [], [4], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "getFront", "getRear", "deleteFront", "deleteLast", "insertFront", "getRear", "deleteLast", "isEmpty"],
            "args": [[2], [], [], [], [], [9], [], [], []]
        }},
    ]


def hidden():
    def gen_random(seed, k, n_ops):
        rng = random.Random(seed)
        ops, args = ["MyCircularDeque"], [[k]]
        methods = ["insertFront", "insertLast", "deleteFront", "deleteLast", "getFront", "getRear", "isEmpty", "isFull"]
        weights = [0.22, 0.22, 0.16, 0.16, 0.08, 0.08, 0.04, 0.04]
        for _ in range(n_ops):
            m = rng.choices(methods, weights=weights, k=1)[0]
            ops.append(m)
            args.append([rng.randint(0, 1000)] if m in ("insertFront", "insertLast") else [])
        return {"in": {"ops": ops, "args": args}}

    # Wrap backward with insertFront + deleteLast
    ops_back, args_back = ["MyCircularDeque"], [[4]]
    for i in range(30):
        ops_back.extend(["insertFront", "getFront", "getRear"])
        args_back.extend([[i], [], []])
        if i >= 3:
            ops_back.append("deleteLast")
            args_back.append([])

    return [
        {"in": {
            "ops": ["MyCircularDeque", "insertFront", "insertLast", "getFront", "getRear", "isFull", "deleteLast", "isEmpty", "insertLast", "getFront", "deleteFront", "isEmpty"],
            "args": [[1], [0], [1], [], [], [], [], [], [1000], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "deleteFront", "deleteLast", "getFront", "getRear", "isEmpty", "isFull"],
            "args": [[4], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "insertFront", "insertFront", "insertFront", "getFront", "getRear", "deleteFront", "getFront", "deleteFront", "getFront", "deleteFront", "getFront"],
            "args": [[3], [10], [20], [30], [], [], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "insertLast", "insertLast", "insertLast", "getFront", "getRear", "deleteLast", "getRear", "deleteLast", "getRear", "deleteLast", "getRear"],
            "args": [[3], [10], [20], [30], [], [], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "insertFront", "insertLast", "insertFront", "insertLast", "getFront", "getRear", "isFull", "deleteFront", "deleteLast", "getFront", "getRear"],
            "args": [[3], [0], [1000], [500], [999], [], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "insertFront", "insertFront", "insertFront", "insertLast", "getFront", "getRear", "deleteFront", "deleteLast", "deleteFront", "isEmpty"],
            "args": [[2], [7], [7], [7], [7], [], [], [], [], [], []]
        }},
        {"in": {
            "ops": ["MyCircularDeque", "insertLast", "insertLast", "deleteFront", "deleteFront", "isEmpty", "insertFront", "insertFront", "getFront", "getRear"],
            "args": [[2], [1], [2], [], [], [], [3], [4], [], []]
        }},
        {"in": {"ops": ops_back, "args": args_back}},
        gen_random(641, 5, 1000),
        gen_random(6410, 50, 1500),
    ]
