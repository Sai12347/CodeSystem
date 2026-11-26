import random


def visible():
    return [
        {"in": {
            "ops": ["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"],
            "args": [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
        }},
        {"in": {
            "ops": ["MyHashMap", "put", "get", "remove", "remove", "get"],
            "args": [[], [0, 0], [0], [999], [0], [0]]
        }},
    ]


def hidden():
    rng = random.Random(706)

    # Collision-heavy test: multiples of 1000, 1024, and 2069
    ops_col = ["MyHashMap"]
    args_col = [[]]
    col_keys = [i * 2069 for i in range(40)] + [i * 1024 for i in range(40)] + [i * 1000 for i in range(40)]
    for idx, k in enumerate(col_keys):
        ops_col.append("put")
        args_col.append([k, idx])
    for k in col_keys[::3]:
        ops_col.append("remove")
        args_col.append([k])
    for k in col_keys:
        ops_col.append("get")
        args_col.append([k])

    # Randomized stress test: 1500 mixed operations
    ops_stress = ["MyHashMap"]
    args_stress = [[]]
    key_pool = [rng.randint(0, 1000000) for _ in range(120)]
    for _ in range(1500):
        op = rng.choices(["put", "get", "remove"], weights=[45, 35, 20])[0]
        k = rng.choice(key_pool)
        ops_stress.append(op)
        if op == "put":
            args_stress.append([k, rng.randint(0, 1000000)])
        else:
            args_stress.append([k])

    return [
        # Empty map gets and removes
        {"in": {
            "ops": ["MyHashMap", "get", "remove", "get"],
            "args": [[], [0], [0], [1000000]]
        }},
        # Max key & value boundaries
        {"in": {
            "ops": ["MyHashMap", "put", "put", "get", "get", "remove", "get", "get"],
            "args": [[], [0, 1000000], [1000000, 0], [0], [1000000], [0], [0], [1000000]]
        }},
        # Repeated overwrites on the same key
        {"in": {
            "ops": ["MyHashMap", "put", "get", "put", "get", "put", "get", "put", "get"],
            "args": [[], [42, 1], [42], [42, 0], [42], [42, 999999], [42], [42, 42], [42]]
        }},
        # Remove then re-insert same key
        {"in": {
            "ops": ["MyHashMap", "put", "remove", "get", "put", "get", "remove", "remove", "get"],
            "args": [[], [7, 100], [7], [7], [7, 200], [7], [7], [7], [7]]
        }},
        # Linked-list head, middle, tail removal within same bucket (mod 2069)
        {"in": {
            "ops": ["MyHashMap", "put", "put", "put", "get", "get", "get",
                    "remove", "get", "get", "get",
                    "remove", "get", "get",
                    "remove", "get"],
            "args": [[], [5, 10], [2074, 20], [4143, 30], [5], [2074], [4143],
                     [2074], [5], [2074], [4143],
                     [4143], [5], [4143],
                     [5], [5]]
        }},
        # Sequential keys 0..20 then remove evens
        {"in": {
            "ops": ["MyHashMap"] + ["put"] * 21 + ["remove"] * 11 + ["get"] * 21,
            "args": [[]] + [[i, i * i] for i in range(21)] + [[i] for i in range(0, 21, 2)] + [[i] for i in range(21)]
        }},
        # Collision-heavy test
        {"in": {"ops": ops_col, "args": args_col}},
        # Randomized stress test
        {"in": {"ops": ops_stress, "args": args_stress}},
    ]
