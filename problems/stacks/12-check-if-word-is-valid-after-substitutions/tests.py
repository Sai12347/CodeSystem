import random


def visible():
    return [
        {"in": {"s": "aabcbc"}},
        {"in": {"s": "abcabcababcc"}},
        {"in": {"s": "abccba"}},
    ]


def _gen_valid(num_triples, rng):
    # Generate a valid string of length 3 * num_triples in O(n) via randomized recursive tree
    # Each node produces "a" + left_child + "b" + mid_child + "c" + right_child (iterative stack).
    out = []
    # Distribute num_triples across nested insertions using an explicit stack of remaining tokens
    stack = [num_triples]
    while stack:
        k = stack.pop()
        if isinstance(k, str):
            out.append(k)
            continue
        if k == 0:
            continue
        # Reserve 1 triple for this wrapper ("a", ..., "b", ..., "c", ...)
        rem = k - 1
        # Split rem among 3 slots: inside a..b, inside b..c, after c
        s1 = rng.randint(0, rem)
        s2 = rng.randint(0, rem - s1)
        s3 = rem - s1 - s2
        # Push in reverse order so output is: "a", s1, "b", s2, "c", s3
        if s3:
            stack.append(s3)
        stack.append("c")
        if s2:
            stack.append(s2)
        stack.append("b")
        if s1:
            stack.append(s1)
        stack.append("a")
    return "".join(out)


def hidden():
    tests = []

    # 1. Minimum length 1 (cannot be valid)
    tests.append({"in": {"s": "a"}})
    tests.append({"in": {"s": "c"}})

    # 2. Length 2 (not a multiple of 3)
    tests.append({"in": {"s": "ab"}})

    # 3. Single valid triple
    tests.append({"in": {"s": "abc"}})

    # 4. Invalid permutation of a, b, c (same counts, wrong order)
    tests.append({"in": {"s": "acb"}})
    tests.append({"in": {"s": "cab"}})

    # 5. Classic trap: equal counts in non-decreasing order "aabbcc" (INVALID!)
    tests.append({"in": {"s": "aabbcc"}})

    # 6. Deep nesting between 'a' and 'b' AND between 'b' and 'c' (VALID)
    tests.append({"in": {"s": "a" * 20 + "bc" * 20}})
    tests.append({"in": {"s": "ab" * 20 + "c" * 20}})

    # 7. Balanced counts with a subtle ordering violation deep inside
    tests.append({"in": {"s": "aababccb" + "c"}})

    # 8. Stress test: valid random nested string of length 6000
    rng1 = random.Random(100301)
    tests.append({"in": {"s": _gen_valid(2000, rng1)}})

    # 9. Stress test: valid length-6000 string with the last 'c' swapped with the nearest non-'c'
    # Keeps equal a/b/c counts and valid prefix, but fails at the very end.
    rng2 = random.Random(100302)
    valid_s = list(_gen_valid(2000, rng2))
    idx = len(valid_s) - 2
    while idx > 0 and valid_s[idx] == "c":
        idx -= 1
    valid_s[idx], valid_s[-1] = valid_s[-1], valid_s[idx]
    tests.append({"in": {"s": "".join(valid_s)}})

    return tests
