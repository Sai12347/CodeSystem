import random


def _traversals_from_edges(n, vals, left, right):
    ino = []
    post = []

    def dfs(u):
        if u == -1:
            return
        dfs(left[u])
        ino.append(vals[u])
        dfs(right[u])
        post.append(vals[u])

    dfs(0)
    return ino, post


def _random_tree_traversals(n: int, seed: int, val_start: int):
    rng = random.Random(seed)
    vals = list(range(val_start, val_start + n))
    rng.shuffle(vals)
    left = [-1] * n
    right = [-1] * n
    available = [0]
    slots = {0: [0, 1]}
    for i in range(1, n):
        idx = rng.randrange(len(available))
        p = available[idx]
        side = slots[p].pop(rng.randrange(len(slots[p])))
        if side == 0:
            left[p] = i
        else:
            right[p] = i
        if not slots[p]:
            available[idx] = available[-1]
            available.pop()
            del slots[p]
        available.append(i)
        slots[i] = [0, 1]
    return _traversals_from_edges(n, vals, left, right)


def _balanced_tree_traversals(vals):
    ino = []
    post = []

    def build(lo, hi):
        if lo > hi:
            return
        mid = (lo + hi) // 2
        build(lo, mid - 1)
        ino.append(vals[mid])
        build(mid + 1, hi)
        post.append(vals[mid])

    build(0, len(vals) - 1)
    return ino, post


def _zigzag_traversals(vals):
    n = len(vals)
    left = [-1] * n
    right = [-1] * n
    for i in range(n - 1):
        if i % 2 == 0:
            left[i] = i + 1
        else:
            right[i] = i + 1
    return _traversals_from_edges(n, vals, left, right)


def visible():
    return [
        {"in": {"inorder": [9, 3, 15, 20, 7], "postorder": [9, 15, 7, 20, 3]}},
        {"in": {"inorder": [-1], "postorder": [-1]}},
        {"in": {"inorder": [2, 1, 3], "postorder": [2, 3, 1]}},
    ]


def hidden():
    left_50 = list(range(1, 51))
    right_50 = list(range(-50, 0))
    zig_in, zig_post = _zigzag_traversals(list(range(-20, 20)))
    comp_in, comp_post = _balanced_tree_traversals(list(range(1, 32)))
    rand_in, rand_post = _random_tree_traversals(800, seed=1061, val_start=-400)
    bal_in, bal_post = _balanced_tree_traversals(list(range(-750, 750)))

    return [
        # Two nodes: left child only
        {"in": {"inorder": [2, 1], "postorder": [2, 1]}},
        # Two nodes: right child only
        {"in": {"inorder": [1, 2], "postorder": [2, 1]}},
        # Extreme boundary values [-3000, 0, 3000]
        {"in": {"inorder": [-3000, 0, 3000], "postorder": [-3000, 3000, 0]}},
        # Left-skewed chain (50 nodes: root=1, left=2, ...)
        {"in": {"inorder": list(reversed(left_50)), "postorder": list(reversed(left_50))}},
        # Right-skewed chain (50 nodes: root=-50, right=-49, ...)
        {"in": {"inorder": right_50, "postorder": list(reversed(right_50))}},
        # Zig-zag tree (40 nodes)
        {"in": {"inorder": zig_in, "postorder": zig_post}},
        # Complete balanced tree (31 nodes)
        {"in": {"inorder": comp_in, "postorder": comp_post}},
        # Asymmetric sparse tree with negative and positive values
        {"in": {"inorder": [-10, -5, 0, 2, 10, 15, 20, 25, 30], "postorder": [-10, 0, 2, -5, 15, 30, 25, 20, 10]}},
        # Stress 1: random tree of 800 nodes
        {"in": {"inorder": rand_in, "postorder": rand_post}},
        # Stress 2: balanced tree of 1500 nodes
        {"in": {"inorder": bal_in, "postorder": bal_post}},
    ]
