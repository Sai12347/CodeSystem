import random


def visible():
    return [
        {"in": {"asteroids": [5, 10, -5]}},
        {"in": {"asteroids": [8, -8]}},
        {"in": {"asteroids": [10, 2, -5]}},
    ]


def hidden():
    tests = []

    # 1. Moving away from each other (negative before positive -> NO collision!)
    tests.append({"in": {"asteroids": [-2, -1, 1, 2]}})

    # 2. All moving right -> no collisions
    tests.append({"in": {"asteroids": [1, 2, 3, 4, 5]}})

    # 3. All moving left -> no collisions
    tests.append({"in": {"asteroids": [-5, -4, -3, -2, -1]}})

    # 4. Single huge left-moving asteroid wipes out many right-moving ones
    tests.append({"in": {"asteroids": [1, 2, 3, 4, 5, 6, 7, 8, -1000]}})

    # 5. Chain of exact mutual cancellations
    tests.append({"in": {"asteroids": [1, 2, 3, 4, -4, -3, -2, -1]}})

    # 6. Minimum length 2 - boundary values +/-1000
    tests.append({"in": {"asteroids": [1000, -1000]}})
    tests.append({"in": {"asteroids": [-1000, 1000]}})

    # 7. Left-moving destroys several, then dies to equal-sized one
    tests.append({"in": {"asteroids": [10, 5, 3, 1, -5]}})

    # 8. Left-moving destroys several, then dies to strictly larger one
    tests.append({"in": {"asteroids": [10, 5, 3, 1, -7]}})

    # 9. Interleaved waves of collisions with surviving negatives and positives
    tests.append({"in": {"asteroids": [-3, 5, -2, 8, -8, -6, 4, -1, -4, 7, -10, 2]}})

    # 10. Stress test: 2000 random non-zero asteroids
    rng1 = random.Random(73501)
    arr1 = []
    for _ in range(2000):
        v = rng1.randint(1, 1000)
        if rng1.random() < 0.5:
            v = -v
        arr1.append(v)
    tests.append({"in": {"asteroids": arr1}})

    # 11. Stress test: worst-case cascade (1500 increasing positives followed by negatives)
    rng2 = random.Random(73502)
    arr2 = [rng2.randint(1, 500) for _ in range(1500)] + [-rng2.randint(1, 1000) for _ in range(500)]
    tests.append({"in": {"asteroids": arr2}})

    return tests
