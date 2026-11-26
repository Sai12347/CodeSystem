def visible():
    return [
        {"in": {"s": "3[a]2[bc]"}},
        {"in": {"s": "3[a2[c]]"}},
        {"in": {"s": "2[abc]3[cd]ef"}},
    ]


def hidden():
    # Stress 1: deep nested expansion -> 50 * (1 + 10 * (1 + 2 * 5)) = 5550 chars
    stress_nested = "50[a10[b5[cd]]]"
    # Stress 2: longer input (length 93 <= 100) with mixed multi-digit counts and 3-level nesting
    stress_long = (
        "12[ab]3[x4[yz]w]15[p2[q]]5[m3[n2[k]]]7[rst]20[u]4[v3[ab2[c]]d]11[ef]2[gh]"
    )

    return [
        {"in": {"s": "z"}},
        {"in": {"s": "leetcode"}},
        {"in": {"s": "1[a]1[b1[c]]"}},
        {"in": {"s": "12[a]"}},
        {"in": {"s": "2[a2[b2[c2[d]]]]"}},
        {"in": {"s": "x2[y3[z]w]q"}},
        {"in": {"s": "10[a]2[b3[c]d]e"}},
        {"in": {"s": "2[a3[b]]3[c2[d]]"}},
        {"in": {"s": "100[ab]"}},
        {"in": {"s": stress_nested}},
        {"in": {"s": stress_long}},
    ]
