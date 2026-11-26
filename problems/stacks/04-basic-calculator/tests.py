import random


def _gen_expr(rng, depth, max_terms):
    parts = []
    n_terms = rng.randint(1, max_terms)
    for i in range(n_terms):
        if i == 0:
            if rng.random() < 0.25:
                parts.append("-")
        else:
            parts.append(rng.choice([" + ", " - ", "+", "-"]))
        if depth > 0 and rng.random() < 0.35:
            parts.append("(" + _gen_expr(rng, depth - 1, max_terms) + ")")
        else:
            parts.append(str(rng.randint(0, 5000)))
    return "".join(parts)


def visible():
    return [
        {"in": {"s": "1 + 1"}},
        {"in": {"s": " 2-1 + 2 "}},
        {"in": {"s": "(1+(4+5+2)-3)+(6+8)"}},
    ]


def hidden():
    rng = random.Random(224)
    # Deeply nested alternating subtraction: 1-(2-(3-...))
    deep_parts = []
    for i in range(1, 401):
        deep_parts.append(f"{i}-(")
    deep_parts.append("401")
    deep_parts.append(")" * 400)
    deep_nested = "".join(deep_parts)

    # Large random valid expression with spaces, parens, unary minus, multi-digit numbers
    chunks = [_gen_expr(rng, 4, 5) for _ in range(40)]
    stress_expr = " + ".join(f"({c})" if idx % 2 == 0 else c for idx, c in enumerate(chunks))
    # Avoid consecutive operators like "+ -..." by wrapping negative chunks in parens
    safe_chunks = []
    for c in chunks:
        if c.startswith("-"):
            safe_chunks.append(f"({c})")
        else:
            safe_chunks.append(c)
    stress_expr = " - ".join(safe_chunks[:20]) + " + " + " + ".join(safe_chunks[20:])

    return [
        {"in": {"s": "0"}},
        {"in": {"s": "   42   "}},
        {"in": {"s": "-1"}},
        {"in": {"s": "-(2 + 3)"}},
        {"in": {"s": "- (3 - (- (4 + 5)))"}},
        {"in": {"s": "2147483647 - 2147483646 + (1000000 - 999999)"}},
        {"in": {"s": "((((((10)))))) - (((((5)))))"}},
        {"in": {"s": "1-(2-(3-(4-(5-6))))"}},
        {"in": {"s": "100 - (50 - (25 - 10) + (30 - (5 + 5))) - (-15)"}},
        {"in": {"s": deep_nested}},
        {"in": {"s": stress_expr}},
    ]
