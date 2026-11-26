import random


def visible():
    return [
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
                "args": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
            }
        },
        {
            "in": {
                "ops": ["LRUCache", "put", "get", "put", "get", "get"],
                "args": [[1], [2, 1], [2], [3, 2], [2], [3]],
            }
        },
    ]


def hidden():
    def gen_stress(seed, cap, num_ops, key_space):
        rng = random.Random(seed)
        ops = ["LRUCache"]
        args = [[cap]]
        for _ in range(num_ops):
            if rng.random() < 0.5:
                ops.append("put")
                args.append([rng.randint(0, key_space), rng.randint(0, 100000)])
            else:
                ops.append("get")
                args.append([rng.randint(0, key_space)])
        return {"in": {"ops": ops, "args": args}}

    return [
        # Empty cache gets only
        {
            "in": {
                "ops": ["LRUCache", "get", "get", "get"],
                "args": [[3], [0], [1], [10000]],
            }
        },
        # Updating existing key refreshes recency and does not evict
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "put", "put", "get", "get", "get"],
                "args": [[2], [1, 10], [2, 20], [1, 100], [3, 30], [1], [2], [3]],
            }
        },
        # Boundary keys and values (0 and max)
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "get", "put", "get", "get"],
                "args": [[2], [0, 0], [10000, 100000], [0], [5, 0], [10000], [5]],
            }
        },
        # Capacity 1 repeated updates on same key then eviction
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "get", "put", "get", "get"],
                "args": [[1], [1, 1], [1, 2], [1], [2, 3], [1], [2]],
            }
        },
        # Capacity 3 with repeated gets on same key (idempotent MRU promotion)
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "put", "get", "get", "put", "get", "get", "get", "get"],
                "args": [[3], [1, 1], [2, 2], [3, 3], [1], [1], [4, 4], [1], [2], [3], [4]],
            }
        },
        # Overwriting existing keys when cache is full must not trigger eviction
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "put", "put", "put", "get", "get", "get"],
                "args": [[3], [1, 1], [2, 2], [3, 3], [2, 20], [1, 10], [3], [2], [1]],
            }
        },
        # Evict then re-insert the evicted key with a new value
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[2], [1, 1], [2, 2], [3, 3], [1], [1, 99], [2], [3], [1]],
            }
        },
        # Large capacity where no evictions occur
        {
            "in": {
                "ops": ["LRUCache", "put", "put", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[100], [1, 10], [2, 20], [3, 30], [4, 40], [2], [2, 25], [1], [2], [4]],
            }
        },
        # Stress: capacity 50, 1500 mixed operations over 120 keys
        gen_stress(146, 50, 1500, 120),
        # Stress: capacity 500, 1500 mixed operations over 1000 keys
        gen_stress(147, 500, 1500, 1000),
    ]
