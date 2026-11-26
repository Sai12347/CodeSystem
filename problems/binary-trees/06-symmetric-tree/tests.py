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



def _make_symmetric(half_nodes, seed, break_one=False):
    rng = random.Random(seed)
    # Build random left subtree of size half_nodes rooted at 1, mirror it at root 2, under root 0
    nodes = {0: [0, 1, 2]}
    nodes[1] = [rng.randint(-10000, 10000), None, None]
    nodes[2] = [nodes[1][0], None, None]
    # pairs of (left_node_id, right_mirror_id, side_on_left)
    slots = [(1, 2, 1), (1, 2, 2)]
    nid = 3
    last_right = 2
    for _ in range(1, half_nodes):
        idx = rng.randrange(len(slots))
        lp, rp, side = slots[idx]
        slots[idx] = slots[-1]
        slots.pop()
        val = rng.randint(-10000, 10000)
        li, ri = nid, nid + 1
        nid += 2
        nodes[li] = [val, None, None]
        nodes[ri] = [val, None, None]
        nodes[lp][side] = li
        nodes[rp][3 - side] = ri
        last_right = ri
        slots.append((li, ri, 1))
        slots.append((li, ri, 2))
    if break_one:
        nodes[last_right][0] = nodes[last_right][0] + 1 if nodes[last_right][0] < 10000 else -10000
    return _serialize({k: tuple(v) for k, v in nodes.items()})


def visible():
    return [
        {"in": {"root": [1, 2, 2, 3, 4, 4, 3]}},
        {"in": {"root": [1, 2, 2, None, 3, None, 3]}},
        {"in": {"root": [1]}},
    ]


def hidden():
    # Deep symmetric V-shape (500 nodes on each arm)
    v_tree = {0: [0, 1, 2]}
    nid = 3
    l_cur, r_cur = 1, 2
    for d in range(499):
        val = (d * 17) % 1000 - 500
        v_tree[l_cur] = [val, nid, None]
        v_tree[r_cur] = [val, None, nid + 1]
        l_cur, r_cur = nid, nid + 1
        nid += 2
    v_tree[l_cur] = [999, None, None]
    v_tree[r_cur] = [999, None, None]

    return [
        {"in": {"root": [1, 2]}},
        {"in": {"root": [1, 2, 2]}},
        {"in": {"root": [1, 2, 3]}},
        # Classic trap: palindromic inorder [2, 2, 1, 2, 2], NOT symmetric
        {"in": {"root": [1, 2, 2, 2, None, 2]}},
        # Sign mismatch deep in tree
        {"in": {"root": [0, -5, -5, 10, -20, -20, -10]}},
        # All-equal values with symmetric sparse structure
        {"in": {"root": [5, 5, 5, None, 5, 5, None, 5, None, None, 5]}},
        # All-equal values with one extra leaf breaking symmetry
        {"in": {"root": [5, 5, 5, None, 5, 5, None, 5, None, None, 5, 5]}},
        {"in": {"root": _serialize({k: tuple(v) for k, v in v_tree.items()})}},
        {"in": {"root": _make_symmetric(1000, 10101, break_one=False)}},
        {"in": {"root": _make_symmetric(1000, 10102, break_one=True)}},
    ]
