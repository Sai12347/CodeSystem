import random


def _gen_disjoint(rng, count, max_step=20, max_len=15):
    res = []
    cur = rng.randint(0, 10)
    for _ in range(count):
        start = cur
        end = start + rng.randint(1, max_len)
        res.append([start, end])
        cur = end + rng.randint(1, max_step)
    return res


def visible():
    return [
        {
            "in": {
                "firstList": [[0, 2], [5, 10], [13, 23], [24, 25]],
                "secondList": [[1, 5], [8, 12], [15, 24], [25, 26]],
            }
        },
        {
            "in": {
                "firstList": [[1, 3], [5, 9]],
                "secondList": [],
            }
        },
        {
            "in": {
                "firstList": [[1, 7]],
                "secondList": [[3, 10]],
            }
        },
    ]


def hidden():
    rng = random.Random(986)
    med_a = _gen_disjoint(rng, 400, max_step=12, max_len=18)
    med_b = _gen_disjoint(rng, 400, max_step=10, max_len=16)

    big_a = _gen_disjoint(rng, 900, max_step=15, max_len=25)
    big_b = _gen_disjoint(rng, 900, max_step=14, max_len=22)

    return [
        {"in": {"firstList": [], "secondList": [[4, 8], [10, 12]]}},
        {"in": {"firstList": [[1, 2], [5, 6]], "secondList": [[3, 4], [7, 8]]}},
        {"in": {"firstList": [[0, 5], [10, 15]], "secondList": [[5, 10], [15, 20]]}},
        {"in": {"firstList": [[0, 3], [5, 8], [10, 12]], "secondList": [[0, 3], [5, 8], [10, 12]]}},
        {
            "in": {
                "firstList": [[0, 1000000000]],
                "secondList": [[1, 2], [10, 20], [500000000, 500000001], [999999998, 1000000000]],
            }
        },
        {
            "in": {
                "firstList": [[1, 5], [8, 12], [15, 18], [20, 25]],
                "secondList": [[0, 30]],
            }
        },
        {
            "in": {
                "firstList": [[0, 500000000], [500000001, 1000000000]],
                "secondList": [[250000000, 750000000]],
            }
        },
        {
            "in": {
                "firstList": [[1, 4], [6, 10], [12, 16], [18, 22]],
                "secondList": [[2, 7], [9, 13], [15, 20]],
            }
        },
        {"in": {"firstList": med_a, "secondList": med_b}},
        {"in": {"firstList": big_a, "secondList": big_b}},
    ]
