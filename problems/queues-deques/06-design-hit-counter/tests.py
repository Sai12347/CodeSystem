import random


def visible():
    return [
        {"in": {
            "ops": ["HitCounter", "hit", "hit", "hit", "getHits", "hit", "getHits", "getHits"],
            "args": [[], [1], [2], [3], [4], [300], [300], [301]]
        }},
        {"in": {
            "ops": ["HitCounter", "hit", "hit", "hit", "getHits", "getHits", "getHits"],
            "args": [[], [10], [10], [10], [10], [309], [310]]
        }},
    ]


def hidden():
    # 50 hits at the same timestamp
    ops_same = ["HitCounter"] + ["hit"] * 50 + ["getHits", "getHits", "getHits"]
    args_same = [[]] + [[100]] * 50 + [[100], [399], [400]]

    # Every second for 350 seconds with periodic queries
    ops_seq, args_seq = ["HitCounter"], [[]]
    for t in range(1, 351):
        ops_seq.append("hit")
        args_seq.append([t])
        if t % 50 == 0:
            ops_seq.append("getHits")
            args_seq.append([t])

    def gen_random(seed, deltas, n_ops):
        rng = random.Random(seed)
        ops, args = ["HitCounter"], [[]]
        t = 1
        for _ in range(n_ops):
            t += rng.choice(deltas)
            if rng.random() < 0.65:
                ops.append("hit")
            else:
                ops.append("getHits")
            args.append([t])
        return {"in": {"ops": ops, "args": args}}

    return [
        {"in": {"ops": ["HitCounter", "getHits", "getHits", "getHits"], "args": [[], [1], [300], [1000]]}},
        {"in": {"ops": ["HitCounter", "hit", "getHits", "getHits", "getHits"], "args": [[], [1], [1], [300], [301]]}},
        {"in": {"ops": ops_same, "args": args_same}},
        {"in": {
            "ops": ["HitCounter", "hit", "hit", "getHits", "getHits", "getHits", "getHits"],
            "args": [[], [1], [300], [300], [301], [599], [600]]
        }},
        {"in": {
            "ops": ["HitCounter", "hit", "hit", "getHits", "hit", "getHits", "getHits"],
            "args": [[], [1999999700], [1999999701], [1999999999], [2000000000], [2000000000], [2000000000]]
        }},
        {"in": {
            "ops": ["HitCounter", "hit", "hit", "getHits", "hit", "hit", "getHits", "getHits"],
            "args": [[], [5], [6], [1000], [1000], [1000], [1000], [1300]]
        }},
        {"in": {
            "ops": ["HitCounter", "hit", "getHits", "hit", "getHits", "hit", "getHits"],
            "args": [[], [50], [50], [50], [50], [50], [50]]
        }},
        {"in": {"ops": ops_seq, "args": args_seq}},
        gen_random(362, [0, 0, 1, 1, 2, 3], 1500),
        gen_random(3620, [0, 1, 5, 25, 100, 350], 1500),
    ]
