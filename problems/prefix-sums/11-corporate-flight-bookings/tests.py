import random


def visible():
    return [
        {"in": {"bookings": [[1, 2, 10], [2, 3, 20], [2, 5, 25]], "n": 5}},
        {"in": {"bookings": [[1, 2, 10], [2, 2, 15]], "n": 2}},
    ]


def hidden():
    rng1 = random.Random(11091)
    stress1 = []
    for _ in range(1500):
        a = rng1.randint(1, 2000)
        b = rng1.randint(a, 2000)
        s = rng1.randint(1, 10000)
        stress1.append([a, b, s])

    rng2 = random.Random(11092)
    stress2 = []
    for _ in range(1500):
        a = rng2.randint(1, 1500)
        b = rng2.randint(1500, 3000)
        s = rng2.randint(1, 10000)
        stress2.append([a, b, s])

    return [
        {"in": {"bookings": [[1, 1, 1]], "n": 1}},
        {"in": {"bookings": [[1, 1, 100], [1, 1, 200], [1, 1, 300]], "n": 1}},
        {"in": {"bookings": [[1, 1, 5], [5, 5, 10]], "n": 6}},
        {"in": {"bookings": [[1, 5, 10000], [1, 5, 10000]], "n": 5}},
        {"in": {"bookings": [[1, 2, 7], [3, 4, 8], [5, 6, 9]], "n": 6}},
        {"in": {"bookings": [[1, 7, 1], [2, 6, 2], [3, 5, 3], [4, 4, 4]], "n": 7}},
        {"in": {"bookings": [[2, 4, 50], [2, 4, 50], [2, 4, 50]], "n": 5}},
        {"in": {"bookings": [[1, 10, 10000]] * 50, "n": 10}},
        {"in": {"bookings": [[1, 3, 5], [2, 5, 10], [4, 4, 15], [1, 5, 20], [3, 5, 25]], "n": 5}},
        {"in": {"bookings": stress1, "n": 2000}},
        {"in": {"bookings": stress2, "n": 3000}},
    ]
