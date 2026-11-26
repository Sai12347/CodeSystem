import random


def _traversals_from_edges(n, vals, left, right):
    pre = []
    ino = []

    def dfs(u):
        if u == -1:
            return
        pre.append(vals[u])
        dfs(left[u])
        ino.append(vals[u])
        dfs(right[u])

    dfs(0)
    return pre, ino


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
    pre = []
    ino = []

    def build(lo, hi):
        if lo > hi:
            return
        mid = (lo + hi) // 2
        pre.append(vals[mid])
        build(lo, mid - 1)
        ino.append(vals[mid])
        build(mid + 1, hi)

    build(0, len(vals) - 1)
    return pre, ino


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
        {"in": {"preorder": [3, 9, 20, 15, 7], "inorder": [9, 3, 15, 20, 7]}},
        {"in": {"preorder": [-1], "inorder": [-1]}},
        {"in": {"preorder": [1, 2, 3], "inorder": [2, 1, 3]}},
    ]


def hidden():
    left_50 = list(range(1, 51))
    right_50 = list(range(-50, 0))
    zig_pre, zig_in = _zigzag_traversals(list(range(-20, 20)))
    comp_pre, comp_in = _balanced_tree_traversals(list(range(1, 32)))
    rand_pre, rand_in = _random_tree_traversals(800, seed=1051, val_start=-400)
    bal_pre, bal_in = _balanced_tree_traversals(list(range(-750, 750)))

    return [
        # Two nodes: left child only
        {"in": {"preorder": [1, 2], "inorder": [2, 1]}},
        # Two nodes: right child only
        {"in": {"preorder": [1, 2], "inorder": [1, 2]}},
        # Extreme boundary values [-3000, 0, 3000]
        {"in": {"preorder": [0, -3000, 3000], "inorder": [-3000, 0, 3000]}},
        # Left-skewed chain (50 nodes)
        {"in": {"preorder": left_50, "inorder": list(reversed(left_50))}},
        # Right-skewed chain (50 nodes)
        {"in": {"preorder": right_50, "inorder": right_50}},
        # Zig-zag tree (40 nodes)
        {"in": {"preorder": zig_pre, "inorder": zig_in}},
        # Complete balanced tree (31 nodes)
        {"in": {"preorder": comp_pre, "inorder": comp_in}},
        # Asymmetric sparse tree with negative and positive values
        {"in": {"preorder": [10, -5, -10, 2, 0, 20, 15, 25, 30], "inorder": [-10, -5, 0, 2, 10, 15, 20, 25, 30]}},
        # Stress 1: random tree of 800 nodes
        {"in": {"preorder": rand_pre, "inorder": rand_in}},
        # Stress 2: balanced tree of 1500 nodes
        {"in": {"preorder": bal_pre, "inorder": bal_in}},
    ]
