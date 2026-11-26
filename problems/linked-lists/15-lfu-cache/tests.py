import random


def visible():
    return [
        {
            "in": {
                "ops": ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"],
                "args": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]],
            }
        },
        {
            "in": {
                "ops": ["LFUCache", "put", "put", "put", "put", "get", "get", "get"],
                "args": [[2], [1, 10], [2, 20], [1, 15], [3, 30], [2], [1], [3]],
            }
        },
    ]


def hidden():
    def gen_stress(seed, cap, num_ops, key_space):
        rng = random.Random(seed)
        ops = ["LFUCache"]
        args = [[cap]]
        for _ in range(num_ops):
            if rng.random() < 0.45:
                ops.append("put")
                args.append([rng.randint(0, key_space), rng.randint(0, 1000000000)])
            else:
                ops.append("get")
                args.append([rng.randint(0, key_space)])
        return {"in": {"ops": ops, "args": args}}

    return [
        # Capacity 1 with gets, overwrites, and evictions
        {
            "in": {
                "ops": ["LFUCache", "put", "get", "put", "get", "put", "get", "get"],
                "args": [[1], [1, 10], [1], [1, 20], [1], [2, 30], [1], [2]],
            }
        },
        # Empty cache lookups
        {
            "in": {
                "ops": ["LFUCache", "get", "get", "get"],
                "args": [[3], [0], [1], [100000]],
            }
        },
        # minFreq rises when all freq-1 keys are promoted, then resets to 1 on new insert
        {
            "in": {
                "ops": ["LFUCache", "put", "put", "get", "get", "put", "get", "get", "get", "put", "get", "get"],
                "args": [[2], [1, 1], [2, 2], [1], [2], [3, 3], [1], [2], [3], [4, 4], [3], [4]],
            }
        },
        # High frequency gap before eviction (keys reach freq 4 and freq 5)
        {
            "in": {
                "ops": [
                    "LFUCache", "put", "put",
                    "get", "get", "get",
                    "get", "get", "get", "get",
                    "put", "get", "get", "get",
                ],
                "args": [
                    [2], [1, 100], [2, 200],
                    [1], [1], [1],
                    [2], [2], [2], [2],
                    [3, 300], [1], [2], [3],
                ],
            }
        },
        # Multi-way tie at frequency 2 broken strictly by LRU order
        {
            "in": {
                "ops": [
                    "LFUCache", "put", "put", "put",
                    "get", "get", "get",
                    "put", "get", "get", "get", "get",
                ],
                "args": [
                    [3], [1, 1], [2, 2], [3, 3],
                    [2], [3], [1],
                    [4, 4], [1], [2], [3], [4],
                ],
            }
        },
        # Updating existing key at full capacity must not evict and must bump its frequency
        {
            "in": {
                "ops": ["LFUCache", "put", "put", "put", "put", "put", "get", "get", "get", "get"],
                "args": [[3], [1, 1], [2, 2], [3, 3], [1, 10], [2, 20], [1], [2], [3], [4]],
            }
        },
        # Extreme constraint values (0 and 10^9, max key 10^5)
        {
            "in": {
                "ops": ["LFUCache", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[2], [0, 0], [100000, 1000000000], [0], [50000, 999999999], [0], [100000], [50000]],
            }
        },
        # Re-inserting an evicted key resets its frequency back to 1
        {
            "in": {
                "ops": [
                    "LFUCache", "put", "put", "get", "get", "get", "get",
                    "put", "get", "put", "put", "get", "get", "get",
                ],
                "args": [
                    [2], [1, 1], [2, 2], [1], [1], [2], [2],
                    [3, 3], [1], [1, 11], [4, 4], [1], [2], [4],
                ],
            }
        },
        # Stress: capacity 30, 1500 mixed operations over 80 keys
        gen_stress(460, 30, 1500, 80),
        # Stress: capacity 200, 1500 mixed operations over 500 keys
        gen_stress(461, 200, 1500, 500),
    ]
