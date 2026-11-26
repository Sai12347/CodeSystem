import random
from collections import deque


def _build_random_tree(n: int, seed: int):
    rng = random.Random(seed)
    vals = [rng.randint(-100, 100) for _ in range(n)]
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
        {"in": {"root": [1, 2, 3, None, 5, None, 4]}},
        {"in": {"root": [1, 2, 3, 4, None, None, None, 5]}},
        {"in": {"root": []}},
    ]


def hidden():
    rng = random.Random(1992)
    balanced_1500 = [rng.randint(-100, 100) for _ in range(1500)]
    return [
        # Single node
        {"in": {"root": [0]}},
        # Right-only skewed tree (30 nodes)
        {"in": {"root": _skewed(list(range(1, 31)), False)}},
        # Left-only skewed tree (30 nodes)
        {"in": {"root": _skewed(list(range(-30, 0)), True)}},
        # Left subtree much deeper than right subtree
        {"in": {"root": [1, 2, 3, 4, 5, None, None, 6, None, None, 7, None, None, 8]}},
        # Zig-zag tree (40 nodes)
        {"in": {"root": _zigzag(list(range(-20, 20)))}},
        # Duplicate and boundary values [-100, 100]
        {"in": {"root": [-100, 100, -100, 0, None, None, 100, -100]}},
        # Complete binary tree (31 nodes)
        {"in": {"root": list(range(1, 32))}},
        # Deepest node hidden on the far left of a wide tree
        {"in": {"root": [10, 20, 30, 40, 50, 60, 70, 80, None, None, None, None, None, None, None, 90]}},
        # Stress 1: random tree of 1000 nodes
        {"in": {"root": _build_random_tree(1000, seed=1991)}},
        # Stress 2: complete/balanced tree of 1500 nodes
        {"in": {"root": balanced_1500}},
    ]
