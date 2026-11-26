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
        {"in": {"root": [1]}},
        {"in": {"root": []}},
    ]


def hidden():
    # Outer-arms tree: deep leaves only on extreme left and extreme right
    arms = {0: (1, 1, 2)}
    l_id, r_id = 1, 2
    nid = 3
    for d in range(6):
        nl, nr = nid, nid + 1
        nid += 2
        arms[l_id] = (-(d + 2), nl if d < 5 else None, None)
        arms[r_id] = (d + 2, None, nr if d < 5 else None)
        l_id, r_id = nl, nr

    return [
        {"in": {"root": [1, 2]}},
        {"in": {"root": [1, None, 2]}},
        {"in": {"root": _skewed_tree(list(range(1, 13)), "left")}},
        {"in": {"root": _skewed_tree(list(range(1, 13)), "right")}},
        {"in": {"root": list(range(1, 32))}},
        {"in": {"root": [4, 4, 4, 4, None, None, 4, 4, 4]}},
        {"in": {"root": [-10000, 0, 10000, -500, None, 500, None, None, -1, 1]}},
        {"in": {"root": _serialize(arms)}},
        {"in": {"root": _random_tree(1800, 10201, -10000, 10000)}},
        {"in": {"root": [((i * 19) % 20001) - 10000 for i in range(1023)]}},
    ]
