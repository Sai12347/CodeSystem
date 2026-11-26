import random


def visible():
    return [
        {"in": {"nums": [3, 10, 5, 25, 2, 8]}},
        {"in": {"nums": [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]}},
    ]


def hidden():
    tests = []

    # 1. Single zero
    tests.append({"in": {"nums": [0]}})

    # 2. Single max int (i == j gives 0)
    tests.append({"in": {"nums": [2147483647]}})

    # 3. All elements equal
    tests.append({"in": {"nums": [42, 42, 42, 42, 42]}})

    # 4. Extremes 0 and 2^31 - 1
    tests.append({"in": {"nums": [0, 2147483647]}})

    # 5. Powers of two
    tests.append({"in": {"nums": [1 << k for k in range(31)]}})

    # 6. Complementary bit patterns yielding 2^31 - 1
    tests.append({"in": {"nums": [0x55555555, 0x2AAAAAAA, 0x12345678, 0x0F0F0F0F, 0x70F0F0F0]}})

    # 7. Sorted ascending 0..63
    tests.append({"in": {"nums": list(range(64))}})

    # 8. Reverse sorted 200..150
    tests.append({"in": {"nums": list(range(200, 149, -1))}})

    # 9. Numbers sharing high bit prefix
    base = 1 << 30
    tests.append({"in": {"nums": [base + x for x in [0, 7, 15, 31, 64, 127, 255, 513, 1020]]}})

    # 10. Deterministic random medium test (n = 500)
    rng = random.Random(42101)
    tests.append({"in": {"nums": [rng.randint(0, (1 << 31) - 1) for _ in range(500)]}})

    # 11. Larger deterministic stress test (n = 2500)
    rng = random.Random(42102)
    tests.append({"in": {"nums": [rng.randint(0, (1 << 31) - 1) for _ in range(2500)]}})

    return tests
