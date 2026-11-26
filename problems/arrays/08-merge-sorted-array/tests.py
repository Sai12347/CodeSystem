import random


def visible():
    return [
        {"in": {"nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [2, 5, 6], "n": 3}},
        {"in": {"nums1": [1], "m": 1, "nums2": [], "n": 0}},
        {"in": {"nums1": [0], "m": 0, "nums2": [1], "n": 1}},
    ]


def hidden():
    rng = random.Random(808)
    a1 = sorted(rng.randint(-10**9, 10**9) for _ in range(1000))
    b1 = sorted(rng.randint(-10**9, 10**9) for _ in range(1000))
    a2 = sorted(rng.randint(-500, 500) for _ in range(1500))
    b2 = sorted(rng.randint(-500, 500) for _ in range(500))
    return [
        {"in": {"nums1": [0, 0, 0], "m": 0, "nums2": [-5, 0, 5], "n": 3}},
        {"in": {"nums1": [-3, -1, 2], "m": 3, "nums2": [], "n": 0}},
        {"in": {"nums1": [4, 5, 6, 0, 0, 0], "m": 3, "nums2": [1, 2, 3], "n": 3}},
        {"in": {"nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [4, 5, 6], "n": 3}},
        {"in": {"nums1": [2, 2, 2, 0, 0], "m": 3, "nums2": [2, 2], "n": 2}},
        {"in": {"nums1": [-10, -5, 0, 0, 0, 0], "m": 3, "nums2": [-7, -5, 0], "n": 3}},
        {"in": {"nums1": [-1000000000, 1000000000, 0, 0], "m": 2, "nums2": [-1000000000, 1000000000], "n": 2}},
        {"in": {"nums1": [1, 3, 5, 7, 9, 0, 0, 0, 0, 0], "m": 5, "nums2": [2, 4, 6, 8, 10], "n": 5}},
        {"in": {"nums1": a1 + [0] * len(b1), "m": len(a1), "nums2": b1, "n": len(b1)}},
        {"in": {"nums1": a2 + [0] * len(b2), "m": len(a2), "nums2": b2, "n": len(b2)}},
    ]
