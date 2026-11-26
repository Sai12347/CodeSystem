import random


def visible():
    return [
        {"in": {"nums1": [1, 2, 2, 1], "nums2": [2, 2]}},
        {"in": {"nums1": [4, 9, 5], "nums2": [9, 4, 9, 8, 4]}},
        {"in": {"nums1": [1, 2, 3], "nums2": [4, 5, 6]}},
    ]


def hidden():
    rng = random.Random(349)
    a_large = [rng.randint(0, 1000) for _ in range(1000)]
    b_large = [rng.randint(0, 1000) for _ in range(1000)]
    evens = [2 * (i % 501) for i in range(1000)]
    odds = [2 * (i % 500) + 1 for i in range(1000)]
    return [
        {"in": {"nums1": [0], "nums2": [0]}},
        {"in": {"nums1": [0], "nums2": [1000]}},
        {"in": {"nums1": [0, 1000, 500, 0], "nums2": [1000, 0, 1000]}},
        {"in": {"nums1": [7, 7, 7, 7], "nums2": [7, 7]}},
        {"in": {"nums1": [1, 2, 3, 4, 5], "nums2": [2, 4]}},
        {"in": {"nums1": list(range(20)), "nums2": list(range(20))}},
        {"in": {"nums1": list(range(30, 0, -1)), "nums2": list(range(15, 45))}},
        {"in": {"nums1": [5], "nums2": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10}},
        {"in": {"nums1": a_large, "nums2": b_large}},
        {"in": {"nums1": evens, "nums2": odds}},
    ]
