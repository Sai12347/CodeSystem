import random
from collections import deque


def _build_random_tree(n: int, seed: int):
    rng = random.Random(seed)
    vals = list(range(n))
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


def _skewed(vals, go_left: bool):
    out = [vals[0]]
    for v in vals[1:]:
        out.extend([v, None] if go_left else [None, v])
    while out and out[-1] is None:
        out.pop()
    return out


def _zigzag(vals):
    out = [vals[0]]
    for i, v in enumerate(vals[1:]):
        out.extend([v, None] if i % 2 == 0 else [None, v])
    while out and out[-1] is None:
        out.pop()
    return out


def visible():
    return [
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "target": 5, "k": 2}},
        {"in": {"root": [1], "target": 1, "k": 3}},
        {"in": {"root": [1, 2, 3], "target": 1, "k": 0}},
    ]


def hidden():
    rand_tree, rand_vals = _build_random_tree(450, seed=8631)
    complete_500 = list(range(500))
    return [
        # Single node with k = 0 and value 0
        {"in": {"root": [0], "target": 0, "k": 0}},
        # Target is leaf, k reaches across root to opposite subtree
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "target": 7, "k": 5}},
        # Target is root, k equals max depth
        {"in": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "target": 3, "k": 3}},
        # k much larger than tree diameter (max constraint k = 1000)
        {"in": {"root": [10, 20, 30, 40, 50], "target": 20, "k": 1000}},
        # k = 1 (immediate parent and both children)
        {"in": {"root": [10, 20, 30, 40, 50, 60, 70], "target": 20, "k": 1}},
        # Left-skewed chain (50 nodes), target in middle, k = 10 goes both ways
        {"in": {"root": _skewed(list(range(50)), True), "target": 25, "k": 10}},
        # Right-skewed chain (50 nodes), target at leaf, k = 49 reaches root
        {"in": {"root": _skewed(list(range(100, 150)), False), "target": 149, "k": 49}},
        # Zig-zag chain (60 nodes), target near top
        {"in": {"root": _zigzag(list(range(200, 260))), "target": 210, "k": 20}},
        # Stress 1: random tree of 450 nodes
        {"in": {"root": rand_tree, "target": rand_vals[200], "k": 5}},
        # Stress 2: complete binary tree of 500 nodes, target is a deep leaf
        {"in": {"root": complete_500, "target": 499, "k": 8}},
    ]
