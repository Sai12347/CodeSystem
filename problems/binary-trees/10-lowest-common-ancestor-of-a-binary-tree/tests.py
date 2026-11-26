import random
from collections import deque


def _build_random_tree(n: int, seed: int, val_start: int = 1):
    rng = random.Random(seed)
    vals = list(range(val_start, val_start + n))
    rng.shuffle(vals)
    # Build level-order array using an explicit parent list so tree stays moderately deep
    left = [-1] * n
    right = [-1] * n
    available = [0]  # indices that still have at least one free child slot
    slots = {0: [0, 1]}
    for i in range(1, n):
        idx = rng.randrange(len(available))
        parent = available[idx]
        side = slots[parent].pop(rng.randrange(len(slots[parent])))
        if side == 0:
            left[parent] = i
        else:
            right[parent] = i
        if not slots[parent]:
            available[idx] = available[-1]
            available.pop()
            del slots[parent]
        available.append(i)
        slots[i] = [0, 1]

    # Serialize to compact level-order list
    out = []
    q = deque([0])
    while q:
        u = q.popleft()
        if u == -1:
            out.append(None)
        else:
            out.append(vals[u])
            q.append(left[u])
            q.append(right[u])
    while out and out[-1] is None:
        out.pop()
    return out, vals


def _skewed_tree(vals, go_left: bool):
    out = [vals[0]]
    for v in vals[1:]:
        if go_left:
            out.extend([v, None])
        else:
            out.extend([None, v])
    while out and out[-1] is None:
        out.pop()
    return out


def _zigzag_tree(vals):
    out = [vals[0]]
    for i, v in enumerate(vals[1:]):
        if i % 2 == 0:
            out.extend([v, None])
        else:
            out.extend([None, v])
    while out and out[-1] is None:
        out.pop()
    return out


def visible():
    return [
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 1}},
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 4}},
        {"in": {"root": [1, 2], "p": 1, "q": 2}},
    ]


def hidden():
    left_vals = list(range(1, 51))
    right_vals = list(range(-50, 0))
    zig_vals = list(range(100, 160))
    rand_tree, rand_vals = _build_random_tree(1200, seed=2361, val_start=-600)
    complete_vals = list(range(1, 2048))

    return [
        # Minimum size right child, reversed p/q
        {"in": {"root": [1, None, 2], "p": 2, "q": 1}},
        # Extreme 32-bit int boundary values
        {"in": {"root": [-1000000000, 1000000000, 0, -5, 5, -999999999, 999999999], "p": -5, "q": 999999999}},
        # Deep siblings where LCA is immediate parent
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 7, "q": 4}},
        # Root and deepest leaf
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 4, "q": 3}},
        # Deep leaves in same subtree (left side)
        {"in": {"root": [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 8], "p": 1, "q": 8}},
        # Left-skewed chain of 50 nodes
        {"in": {"root": _skewed_tree(left_vals, True), "p": 15, "q": 50}},
        # Right-skewed chain of 50 nodes
        {"in": {"root": _skewed_tree(right_vals, False), "p": -1, "q": -25}},
        # Zig-zag chain of 60 nodes
        {"in": {"root": _zigzag_tree(zig_vals), "p": 159, "q": 130}},
        # Stress 1: random tree with 1200 nodes
        {"in": {"root": rand_tree, "p": rand_vals[400], "q": rand_vals[1199]}},
        # Stress 2: complete binary tree with 2047 nodes (deep leaves in left half)
        {"in": {"root": complete_vals, "p": 1024, "q": 1535}},
    ]
