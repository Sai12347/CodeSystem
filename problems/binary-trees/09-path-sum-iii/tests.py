from collections import deque
import random


def _serialize(nodes):
    """Serialize a dict-based tree {id: (val, left_id, right_id)} rooted at 0 into LeetCode level-order list."""
    if not nodes or 0 not in nodes:
        return []
    out = []
    q = deque([0])
    while q:
        u = q.popleft()
        if u is None:
            out.append(None)
            continue
        val, l, r = nodes[u]
        out.append(val)
        q.append(l)
        q.append(r)
    while out and out[-1] is None:
        out.pop()
    return out


def _random_tree(n, seed, lo=-1000, hi=1000):
    rng = random.Random(seed)
    if n <= 0:
        return []
    nodes = {0: [rng.randint(lo, hi), None, None]}
    open_slots = [(0, 1), (0, 2)]
    for i in range(1, n):
        idx = rng.randrange(len(open_slots))
        parent, side = open_slots[idx]
        open_slots[idx] = open_slots[-1]
        open_slots.pop()
        nodes[i] = [rng.randint(lo, hi), None, None]
        nodes[parent][side] = i
        open_slots.append((i, 1))
        open_slots.append((i, 2))
    return _serialize({k: tuple(v) for k, v in nodes.items()})


def _skewed_tree(vals, direction="left"):
    if not vals:
        return []
    nodes = {}
    for i, v in enumerate(vals):
        nxt = i + 1 if i + 1 < len(vals) else None
        if direction == "left":
            nodes[i] = (v, nxt, None)
        elif direction == "right":
            nodes[i] = (v, None, nxt)
        else:
            nodes[i] = (v, nxt, None) if i % 2 == 0 else (v, None, nxt)
    return _serialize(nodes)


def visible():
    return [
        {"in": {"root": [10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], "targetSum": 8}},
        {"in": {"root": [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], "targetSum": 22}},
        {"in": {"root": [], "targetSum": 0}},
    ]


def hidden():
    return [
        {"in": {"root": [5], "targetSum": 5}},
        {"in": {"root": [5], "targetSum": 0}},
        # Overlapping zero-sum paths along a chain of 10 zeros -> 55
        {"in": {"root": _skewed_tree([0] * 10, "left"), "targetSum": 0}},
        # Negative nodes and negative target
        {"in": {"root": [-2, None, -3], "targetSum": -5}},
        # Alternating +1/-1 chain with many overlapping subpaths
        {"in": {"root": _skewed_tree([1 if i % 2 == 0 else -1 for i in range(20)], "right"), "targetSum": 0}},
        # 32-bit signed integer overflow trap: 10^9 + 10^9 + 294967296 + 10^9 + 10^9 == 2^32 (wraps to 0 in int32!)
        {"in": {"root": [1000000000, 1000000000, None, 294967296, None, 1000000000, None, 1000000000, None, 1000000000], "targetSum": 0}},
        # Large negative values near -10^9
        {"in": {"root": [-1000000000, -1000000000, 1000000000, None, 1000000000, -1000000000, None], "targetSum": -1000000000}},
        # Sibling leakage trap: 2 + 3 == 5 across siblings is NOT a downward path
        {"in": {"root": [1, 2, 3], "targetSum": 5}},
        # Stress test 1: large random tree with small values so many paths match
        {"in": {"root": _random_tree(900, 43701, -5, 5), "targetSum": 7}},
        # Stress test 2: skewed chain of 800 ones with targetSum = 100 -> 701 paths
        {"in": {"root": _skewed_tree([1] * 800, "left"), "targetSum": 100}},
    ]
