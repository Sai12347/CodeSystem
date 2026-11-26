import random


def visible():
    return [
        {"in": {"s": "abbaca"}},
        {"in": {"s": "azxxzy"}},
        {"in": {"s": "aabb"}},
    ]


def hidden():
    tests = []

    # 1. Single character
    tests.append({"in": {"s": "a"}})

    # 2. Two identical characters -> empty string
    tests.append({"in": {"s": "zz"}})

    # 3. Two different characters -> unchanged
    tests.append({"in": {"s": "ab"}})

    # 4. Odd vs even run of the same character
    tests.append({"in": {"s": "aaaaaaa"}})
    tests.append({"in": {"s": "aaaaaaaa"}})

    # 5. Deeply nested palindrome that collapses completely
    half = "abcdefghijklmnopqrstuvwxyz"
    tests.append({"in": {"s": half + half[::-1]}})

    # 6. Deeply nested palindrome with a middle character surviving
    tests.append({"in": {"s": "abcde" + "z" + "edcba"}})

    # 7. Triple duplicates interleaved (only pairs cancel, not triples!)
    tests.append({"in": {"s": "aaabbbccc"}})

    # 8. No adjacent duplicates at all
    tests.append({"in": {"s": "abababababab"}})

    # 9. Multiple cascading collapses separated by survivors
    tests.append({"in": {"s": "abccba" + "x" + "deffed" + "y" + "ghhg"}})

    # 10. Stress test: large nested collapse (length 4000)
    rng1 = random.Random(104701)
    letters = [chr(ord("a") + rng1.randrange(26)) for _ in range(2000)]
    tests.append({"in": {"s": "".join(letters) + "".join(reversed(letters))}})

    # 11. Stress test: large random string over small alphabet (frequent cascades, length 8000)
    rng2 = random.Random(104702)
    s_rand = "".join(rng2.choice("abcd") for _ in range(8000))
    tests.append({"in": {"s": s_rand}})

    return tests
