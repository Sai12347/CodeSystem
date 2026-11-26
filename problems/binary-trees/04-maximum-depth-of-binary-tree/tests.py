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
        {"in": {"root": [3, 9, 20, None, None, 15, 7]}},
        {"in": {"root": [1, None, 2]}},
        {"in": {"root": []}},
    ]


def hidden():
    # Complete tree of 15 nodes with a 20-node tail hanging off node 10
    tail_tree = {}
    for i in range(15):
        l = 2 * i + 1 if 2 * i + 1 < 15 else None
        r = 2 * i + 2 if 2 * i + 2 < 15 else None
        tail_tree[i] = [i - 7, l, r]
    cur = 10
    for j in range(15, 35):
        tail_tree[cur][1] = j
        tail_tree[j] = [j, None, None]
        cur = j

    # Shallow left (depth 2), deep right (depth 10)
    asym = {0: (0, 1, 2), 1: (-1, None, None)}
    for k in range(2, 11):
        asym[k] = (k, None, k + 1 if k < 10 else None)

    return [
        {"in": {"root": [0]}},
        {"in": {"root": _skewed_tree(list(range(1, 21)), "left")}},
        {"in": {"root": _skewed_tree(list(range(1, 26)), "right")}},
        {"in": {"root": list(range(1, 64))}},
        {"in": {"root": _serialize(asym)}},
        {"in": {"root": [-5, -5, -5, -5, -5, -5, -5]}},
        {"in": {"root": _skewed_tree(list(range(-15, 15)), "zigzag")}},
        {"in": {"root": _serialize({k: tuple(v) for k, v in tail_tree.items()})}},
        {"in": {"root": _random_tree(2500, 10401, -10000, 10000)}},
        {"in": {"root": _skewed_tree([((i * 41) % 20001) - 10000 for i in range(1500)], "left")}},
    ]
