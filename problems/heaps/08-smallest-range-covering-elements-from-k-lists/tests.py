import random


def visible():
    return [
        {"in": {"nums": [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]}},
        {"in": {"nums": [[1, 2, 3], [1, 2, 3], [1, 2, 3]]}},
        {"in": {"nums": [[1, 5], [3, 7]]}},
    ]


def hidden():
    rng1 = random.Random(63201)
    stress1 = [sorted(rng1.randint(-5000, 5000) for _ in range(35)) for _ in range(45)]

    rng2 = random.Random(63202)
    stress2 = [sorted(rng2.randint(-100000, 100000) for _ in range(50)) for _ in range(30)]

    return [
        {"in": {"nums": [[42]]}},
        {"in": {"nums": [[-10, 0, 10, 20]]}},
        {"in": {"nums": [[5], [5], [5], [5]]}},
        {"in": {"nums": [[-100000], [0], [100000]]}},
        {"in": {"nums": [[-5, -4, -3, -2, -1], [1, 2, 3, 4, 5]]}},
        {"in": {"nums": [[1, 1, 1, 5], [2, 2, 6], [3, 7]]}},
        {"in": {"nums": [[10, 10], [11, 11]]}},
        {"in": {"nums": [[-10, -5, 0, 5, 10], [-8, -2, 4, 8], [-9, -3, 3, 9]]}},
        {"in": {"nums": [[1, 5, 8], [4, 12], [7, 8, 10]]}},
        {"in": {"nums": stress1}},
        {"in": {"nums": stress2}},
    ]
