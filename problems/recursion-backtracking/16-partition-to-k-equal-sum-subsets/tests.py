def visible():
    return [
        {"in": {"nums": [4, 3, 2, 3, 5, 2, 1], "k": 4}},
        {"in": {"nums": [1, 2, 3, 4], "k": 3}},
        {"in": {"nums": [2, 2, 2, 2, 3, 4, 5], "k": 4}},
    ]


def hidden():
    return [
        # Single element, k = 1
        {"in": {"nums": [7], "k": 1}},
        # k = 1 always possible
        {"in": {"nums": [1, 5, 9, 2], "k": 1}},
        # k = n all equal
        {"in": {"nums": [5, 5, 5, 5, 5], "k": 5}},
        # k = n not all equal
        {"in": {"nums": [5, 5, 5, 5, 6], "k": 5}},
        # Sum divisible by k, but max element exceeds target
        {"in": {"nums": [10, 1, 1], "k": 3}},
        # Greedy trap: requires exact pairing (target = 14)
        {"in": {"nums": [4, 4, 6, 2, 3, 8, 10, 2, 10, 7], "k": 4}},
        # Boundary large values (10^4)
        {"in": {"nums": [10000, 10000, 5000, 5000, 10000], "k": 4}},
        # Many duplicates, divisible sum, impossible
        {"in": {"nums": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3], "k": 8}},
        # Max length n = 16, high k = 8 (pairs summing to 17)
        {"in": {"nums": [1, 16, 2, 15, 3, 14, 4, 13, 5, 12, 6, 11, 7, 10, 8, 9], "k": 8}},
        # Max length n = 16, k = 4 (True: 4 buckets of 100)
        {"in": {"nums": [25, 31, 19, 25, 42, 18, 22, 18, 37, 29, 14, 20, 50, 15, 23, 12], "k": 4}},
        # Max length n = 16 adversarial stress test (sum=22120, k=5, target=4424)
        {"in": {"nums": [3522, 181, 521, 515, 304, 123, 2512, 312, 922, 407, 146, 1932, 4037, 2646, 3871, 269], "k": 5}},
    ]
