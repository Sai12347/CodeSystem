import random
from collections import deque


def _build_random_tree(n: int, seed: int):
    rng = random.Random(seed)
    vals = [rng.randint(-1000, 1000) for _ in range(n)]
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
    return out


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
        {"in": {"root": [1, 2, 3, None, None, 4, 5]}},
        {"in": {"root": []}},
        {"in": {"root": [1]}},
    ]


def hidden():
    rng = random.Random(2972)
    complete_2047 = [rng.randint(-1000, 1000) for _ in range(2047)]
    return [
        # Duplicate values everywhere
        {"in": {"root": [1, 1, 1, 1, None, None, 1, None, 1]}},
        # Extreme negative, zero, and positive boundaries
        {"in": {"root": [-1000, 1000, 0, -1000, None, 0, 1000]}},
        # Two nodes: left child
        {"in": {"root": [5, -5]}},
        # Two nodes: right child
        {"in": {"root": [5, None, -5]}},
        # Left-skewed chain (40 nodes)
        {"in": {"root": _skewed(list(range(-20, 20)), True)}},
        # Right-skewed chain (40 nodes)
        {"in": {"root": _skewed(list(range(40, 0, -1)), False)}},
        # Zig-zag chain (40 nodes)
        {"in": {"root": _zigzag(list(range(-100, -60)))}},
        # Sparse deep tree with gaps on both sides
        {"in": {"root": [0, -1, 2, None, -3, 4, None, -5, None, None, 6, None, -7, 8]}},
        # Stress 1: random tree of 1000 nodes with duplicates & negatives
        {"in": {"root": _build_random_tree(1000, seed=2971)}},
        # Stress 2: complete binary tree of 2047 nodes
        {"in": {"root": complete_2047}},
    ]
