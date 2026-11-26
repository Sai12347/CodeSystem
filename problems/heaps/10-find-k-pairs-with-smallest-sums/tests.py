import random


def visible():
    return [
        {"in": {"nums1": [1, 7, 11], "nums2": [2, 4, 6], "k": 3}},
        {"in": {"nums1": [1, 1, 2], "nums2": [1, 2, 3], "k": 2}},
        {"in": {"nums1": [1, 2], "nums2": [1, 2], "k": 2}},
    ]


def hidden():
    rng1 = random.Random(37301)
    s1_a = sorted(rng1.randint(-10000, 10000) for _ in range(800))
    s1_b = sorted(rng1.randint(-10000, 10000) for _ in range(800))

    rng2 = random.Random(37302)
    s2_a = sorted(rng2.randint(-50, 50) for _ in range(600))
    s2_b = sorted(rng2.randint(-50, 50) for _ in range(600))

    return [
        {"in": {"nums1": [5], "nums2": [-3], "k": 1}},
        {"in": {"nums1": [1, 2], "nums2": [3], "k": 2}},
        {"in": {"nums1": [1, 1, 2], "nums2": [1, 2, 3], "k": 9}},
        {"in": {"nums1": [0, 0, 0], "nums2": [0, 0, 0], "k": 5}},
        {"in": {"nums1": [-1000000000, 0, 1000000000], "nums2": [-1000000000, 0, 1000000000], "k": 6}},
        {"in": {"nums1": [-10, -4, 0, 0, 6], "nums2": [3, 5, 6, 7, 8, 100], "k": 10}},
        {"in": {"nums1": [1, 2, 4, 5, 6], "nums2": [3, 5, 7, 9], "k": 3}},
        {"in": {"nums1": [1, 100, 200, 300], "nums2": [1, 2, 3, 4, 5], "k": 5}},
        {"in": {"nums1": s1_a, "nums2": s1_b, "k": 250}},
        {"in": {"nums1": s2_a, "nums2": s2_b, "k": 200}},
    ]
