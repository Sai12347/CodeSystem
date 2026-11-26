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



def _off_root_tree(stem_len, branch_a, branch_b, side="left"):
    """Root has a short stem leading to a fork with two long branches (diameter misses root)."""
    nodes = {}
    nid = 0
    for i in range(stem_len):
        if side == "left":
            nodes[i] = [i, i + 1, None]
        else:
            nodes[i] = [i, None, i + 1]
    fork = stem_len
    nid = fork + 1
    l_start = nid
    for j in range(branch_a):
        nxt = nid + 1 if j + 1 < branch_a else None
        nodes[nid] = [nid, nxt, None]
        nid += 1
    r_start = nid
    for j in range(branch_b):
        nxt = nid + 1 if j + 1 < branch_b else None
        nodes[nid] = [nid, None, nxt]
        nid += 1
    nodes[fork] = [fork, l_start, r_start]
    # Add a small opposite child on root so root has both subtrees
    if stem_len > 0:
        if side == "left":
            nodes[0][2] = nid
        else:
            nodes[0][1] = nid
        nodes[nid] = [-1, None, None]
    return _serialize({k: tuple(v) for k, v in nodes.items()})


def visible():
    return [
        {"in": {"root": [1, 2, 3, 4, 5]}},
        {"in": {"root": [1, 2]}},
        {"in": {"root": [1]}},
    ]


def hidden():
    # Asymmetric V-shape from root: left chain 10, right chain 15 -> diameter 25
    v_nodes = {0: (0, 1, 11)}
    for i in range(1, 11):
        v_nodes[i] = (-i, i + 1 if i < 10 else None, None)
    for i in range(11, 26):
        v_nodes[i] = (i, None, i + 1 if i < 25 else None)

    return [
        # Diameter strictly inside left subtree (does not pass through root)
        {"in": {"root": _off_root_tree(1, 5, 5, "left")}},
        # Diameter strictly inside right subtree
        {"in": {"root": _off_root_tree(2, 6, 7, "right")}},
        {"in": {"root": _skewed_tree(list(range(1, 21)), "left")}},
        {"in": {"root": _skewed_tree(list(range(1, 26)), "right")}},
        {"in": {"root": list(range(1, 32))}},
        {"in": {"root": [-7, -7, -7, -7, None, None, -7, -7, -7]}},
        {"in": {"root": _serialize(v_nodes)}},
        {"in": {"root": [4, -7, -3, None, None, -9, -3, 9, -7, -4, None, 6, None, -6, -6, None, None, 0, 6, 5, None, 9, None, None, -1, -4, None, None, None, -2]}},
        {"in": {"root": _random_tree(2000, 54301, -10000, 10000)}},
        {"in": {"root": _off_root_tree(10, 700, 750, "left")}},
    ]
