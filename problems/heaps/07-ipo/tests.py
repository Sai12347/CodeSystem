import random


def visible():
    return [
        {"in": {"k": 2, "w": 0, "profits": [1, 2, 3], "capital": [0, 1, 1]}},
        {"in": {"k": 3, "w": 0, "profits": [1, 2, 3], "capital": [0, 1, 2]}},
        {"in": {"k": 2, "w": 0, "profits": [10, 20], "capital": [1, 2]}},
    ]


def hidden():
    rng1 = random.Random(50201)
    n1 = 2000
    cap1 = [rng1.randint(0, 50000) for _ in range(n1)]
    prof1 = [rng1.randint(0, 10000) for _ in range(n1)]

    # Stress 2: cascading chain where each project unlocks the next batch
    rng2 = random.Random(50202)
    n2 = 1500
    cap2 = [i * 5 for i in range(n2)]
    prof2 = [rng2.randint(4, 15) for _ in range(n2)]
    order2 = list(range(n2))
    rng2.shuffle(order2)
    cap2 = [cap2[i] for i in order2]
    prof2 = [prof2[i] for i in order2]

    return [
        {"in": {"k": 1, "w": 0, "profits": [5], "capital": [0]}},
        {"in": {"k": 10, "w": 0, "profits": [1, 2, 3], "capital": [0, 0, 0]}},
        {"in": {"k": 2, "w": 5, "profits": [0, 0, 0], "capital": [0, 1, 5]}},
        {"in": {"k": 1, "w": 2, "profits": [1, 2, 3], "capital": [1, 1, 2]}},
        {"in": {"k": 4, "w": 1, "profits": [2, 5, 10, 100, 3], "capital": [1, 3, 8, 18, 2]}},
        {"in": {"k": 3, "w": 1000000000, "profits": [10000, 9999, 9998, 1], "capital": [1000000000, 999999999, 0, 500]}},
        {"in": {"k": 5, "w": 10, "profits": [1, 2, 100, 3, 4], "capital": [0, 0, 100, 0, 0]}},
        {"in": {"k": 3, "w": 0, "profits": [10, 10, 10, 10], "capital": [0, 10, 20, 30]}},
        {"in": {"k": 1000, "w": 500, "profits": prof1, "capital": cap1}},
        {"in": {"k": 1500, "w": 0, "profits": prof2, "capital": cap2}},
    ]
