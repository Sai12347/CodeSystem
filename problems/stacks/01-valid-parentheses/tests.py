import random


def _gen_valid(rng, pairs):
    openers = "([{"
    closers = {"(": ")", "[": "]", "{": "}"}
    stack = []
    out = []
    remaining_opens = pairs
    while remaining_opens > 0 or stack:
        if remaining_opens > 0 and (not stack or rng.random() < 0.55):
            ch = rng.choice(openers)
            out.append(ch)
            stack.append(closers[ch])
            remaining_opens -= 1
        else:
            out.append(stack.pop())
    return "".join(out)


def visible():
    return [
        {"in": {"s": "()"}},
        {"in": {"s": "()[]{}"}},
        {"in": {"s": "(]"}},
    ]


def hidden():
    rng = random.Random(20)
    long_valid = _gen_valid(rng, 2000)
    long_invalid_list = list(_gen_valid(rng, 2000))
    mid = len(long_invalid_list) // 2
    flip = {"(": "[", "[": "{", "{": "(", ")": "]", "]": "}", "}": ")"}
    long_invalid_list[mid] = flip[long_invalid_list[mid]]
    long_invalid = "".join(long_invalid_list)
    deep_valid = "(" * 2000 + ")" * 2000

    return [
        {"in": {"s": "("}},
        {"in": {"s": "]"}},
        {"in": {"s": "({[()]})"}},
        {"in": {"s": "([)]"}},
        {"in": {"s": "((("}},
        {"in": {"s": "()[]}"}},
        {"in": {"s": "({[]})("}},
        {"in": {"s": "[({})]([]){{}}"}},
        {"in": {"s": long_valid}},
        {"in": {"s": long_invalid}},
        {"in": {"s": deep_valid}},
    ]
