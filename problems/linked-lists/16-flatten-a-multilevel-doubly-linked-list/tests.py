import random


def visible():
    return [
        {"in": {"head": [1, 2, 3, [7, 8, [11, 12], 9, 10], 4, 5, 6]}},
        {"in": {"head": [1, [3], 2]}},
        {"in": {"head": []}},
    ]


def hidden():
    def build_random_multilevel(seed, target_nodes, max_depth):
        rng = random.Random(seed)
        remaining = [target_nodes]

        def gen_level(depth):
            level = []
            # Create at least 1 node for this level
            length = rng.randint(1, min(6, remaining[0]))
            for _ in range(length):
                if remaining[0] <= 0:
                    break
                remaining[0] -= 1
                level.append(rng.randint(1, 100000))
                if depth < max_depth and remaining[0] > 0 and rng.random() < 0.35:
                    level.append(gen_level(depth + 1))
            return level

        root = []
        while remaining[0] > 0:
            remaining[0] -= 1
            root.append(rng.randint(1, 100000))
            if remaining[0] > 0 and rng.random() < 0.35:
                root.append(gen_level(1))
        return root

    def build_deep_chain(seed, total_nodes, depth):
        rng = random.Random(seed)
        # First create a deep vertical chain of `depth` nodes, then append remaining nodes on top level
        chain = [rng.randint(1, 100000)]
        for _ in range(depth - 1):
            chain = [rng.randint(1, 100000), chain]
        rest_count = total_nodes - depth
        top = [rng.randint(1, 100000) for _ in range(rest_count // 2)]
        top.extend(chain)
        top.extend(rng.randint(1, 100000) for _ in range(rest_count - rest_count // 2))
        return top

    return [
        # Single node
        {"in": {"head": [42]}},
        # Flat doubly linked list with no children
        {"in": {"head": [1, 2, 3, 4, 5]}},
        # Purely vertical child chain (no next pointers on any level)
        {"in": {"head": [1, [2, [3, [4, [5, [6]]]]]]}},
        # Child attached to the tail node of each level
        {"in": {"head": [1, 2, 3, [4, 5, [6, 7]]]}},
        # Child attached to the head node of each level
        {"in": {"head": [1, [2, 3, [4]], 5, 6]}},
        # Multiple siblings on the same level each having children
        {"in": {"head": [1, [10, 11], 2, [20, [21, 22], 23], 3, [30]]}},
        # All duplicate values across multiple levels
        {"in": {"head": [5, [5, [5], 5], 5, [5]]}},
        # Extreme constraint values (1 and 100000)
        {"in": {"head": [100000, [1, [100000]], 1]}},
        # Stress: 600 nodes random branching multilevel structure
        {"in": {"head": build_random_multilevel(430, 600, 10)}},
        # Stress: 1000 nodes with deep vertical child chain of depth 200
        {"in": {"head": build_deep_chain(431, 1000, 200)}},
    ]
