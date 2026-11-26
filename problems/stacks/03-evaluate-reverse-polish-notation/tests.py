import random


def _gen_rpn(rng, num_ops):
    tokens = []
    sim = []
    ops_left = num_ops
    # Build a valid RPN expression while keeping intermediate values well inside 32-bit int
    # and strictly avoiding division by zero.
    val = rng.randint(-200, 200)
    tokens.append(str(val))
    sim.append(val)
    while ops_left > 0:
        if len(sim) < 2 or (len(sim) < 12 and rng.random() < 0.55 and ops_left > len(sim) - 1):
            v = rng.randint(-200, 200)
            tokens.append(str(v))
            sim.append(v)
        else:
            b = sim[-1]
            a = sim[-2]
            candidates = ["+", "-"]
            if abs(a * b) <= 10**9:
                candidates.append("*")
            if b != 0:
                candidates.append("/")
            op = rng.choice(candidates)
            sim.pop()
            sim.pop()
            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            elif op == "*":
                res = a * b
            else:
                res = int(a / b)
            if abs(res) > 10**9:
                # Fallback to safe addition/subtraction
                op = "-" if (a > 0 and b > 0) or (a < 0 and b < 0) else "+"
                res = a - b if op == "-" else a + b
            tokens.append(op)
            sim.append(res)
            ops_left -= 1
    while len(sim) > 1:
        b = sim.pop()
        a = sim.pop()
        if abs(a + b) <= 10**9:
            tokens.append("+")
            sim.append(a + b)
        else:
            tokens.append("-")
            sim.append(a - b)
    return tokens


def visible():
    return [
        {"in": {"tokens": ["2", "1", "+", "3", "*"]}},
        {"in": {"tokens": ["4", "13", "5", "/", "+"]}},
        {"in": {"tokens": ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]}},
    ]


def hidden():
    rng = random.Random(150)
    stress_mixed = _gen_rpn(rng, 1000)

    stress_chain = ["200"]
    for i in range(1000):
        stress_chain.append(str(-200 if i % 2 == 0 else 200))
        stress_chain.append("-" if i % 3 == 0 else "+")

    return [
        {"in": {"tokens": ["42"]}},
        {"in": {"tokens": ["-200"]}},
        {"in": {"tokens": ["5", "3", "-"]}},
        {"in": {"tokens": ["-7", "2", "/", "7", "-2", "/", "+", "-7", "-2", "/", "+"]}},
        {"in": {"tokens": ["0", "3", "-", "5", "-", "-2", "*"]}},
        {"in": {"tokens": ["0", "200", "/", "150", "0", "*", "+"]}},
        {"in": {"tokens": ["1", "2", "3", "4", "5", "+", "-", "*", "/"]}},
        {"in": {"tokens": ["200", "200", "*", "200", "*", "200", "*"]}},
        {"in": {"tokens": ["-200", "200", "*", "200", "*", "200", "*", "200", "/", "-1", "*"]}},
        {"in": {"tokens": stress_mixed}},
        {"in": {"tokens": stress_chain}},
    ]
