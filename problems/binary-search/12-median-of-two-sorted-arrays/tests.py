import random


def visible():
    return [
        {"in": {"nums1": [1, 3], "nums2": [2]}},
        {"in": {"nums1": [1, 2], "nums2": [3, 4]}},
        {"in": {"nums1": [], "nums2": [1]}},
    ]


def hidden():
    rng1 = random.Random(401)
    s1_a = sorted(rng1.randint(-1000000, 1000000) for _ in range(1000))
    s1_b = sorted(rng1.randint(-1000000, 1000000) for _ in range(999))

    rng2 = random.Random(402)
    s2_a = sorted(rng2.randint(-1000000, 1000000) for _ in range(1000))
    s2_b = sorted(rng2.randint(-1000000, 1000000) for _ in range(1000))

    return [
        {"in": {"nums1": [2, 5, 9], "nums2": []}},
        {"in": {"nums1": [], "nums2": [-5, -1, 3, 10]}},
        {"in": {"nums1": [-1000000], "nums2": [1000000]}},
        {"in": {"nums1": [-10, -8, -5], "nums2": [-9, -3, -1]}},
        {"in": {"nums1": [7, 7, 7, 7], "nums2": [7, 7, 7]}},
        {"in": {"nums1": [1, 2, 3, 4, 5], "nums2": [100, 200, 300]}},
        {"in": {"nums1": [50, 60, 70], "nums2": [1, 2, 3, 4, 5, 6]}},
        {"in": {"nums1": [1, 2, 2, 5, 6, 8, 9], "nums2": [2, 3, 7]}},
        {"in": {"nums1": s1_a, "nums2": s1_b}},
        {"in": {"nums1": s2_a, "nums2": s2_b}},
    ]
