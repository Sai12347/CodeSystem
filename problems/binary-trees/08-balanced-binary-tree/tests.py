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



def _fib_avl(h):
    """Build a minimal-node height-balanced (Fibonacci/AVL) tree of height h."""
    nodes = {}
    counter = [0]

    def build(height):
        if height <= 0:
            return None
        nid = counter[0]
        counter[0] += 1
        l = build(height - 1)
        r = build(height - 2)
        nodes[nid] = [nid, l, r]
        return nid

    build(h)
    return nodes


def visible():
    return [
        {"in": {"root": [3, 9, 20, None, None, 15, 7]}},
        {"in": {"root": [1, 2, 2, 3, 3, None, None, 4, 4]}},
        {"in": {"root": []}},
    ]


def hidden():
    fib_ok = _fib_avl(9)  # 88 nodes, every internal node has height diff 1 -> True
    fib_bad = _fib_avl(9)
    # Attach two extra chained nodes to a deep leaf to create an imbalance at depth
    deepest = max(k for k, v in fib_bad.items() if v[1] is None and v[2] is None)
    n1 = len(fib_bad)
    n2 = n1 + 1
    fib_bad[deepest][1] = n1
    fib_bad[n1] = [n1, n2, None]
    fib_bad[n2] = [n2, None, None]

    # Large complete tree (1023 nodes) with a 2-node tail on one leaf -> unbalanced at bottom
    almost_bal = {}
    for i in range(1023):
        l = 2 * i + 1 if 2 * i + 1 < 1023 else None
        r = 2 * i + 2 if 2 * i + 2 < 1023 else None
        almost_bal[i] = [((i * 13) % 2001) - 1000, l, r]
    almost_bal[1022][1] = 1023
    almost_bal[1023] = [1, 1024, None]
    almost_bal[1024] = [2, None, None]

    return [
        {"in": {"root": [1]}},
        {"in": {"root": [1, 2]}},
        {"in": {"root": [1, 2, None, 3]}},
        # Classic trap: root left & right heights are both 3, but inner subtrees are unbalanced
        {"in": {"root": [1, 2, 2, 3, None, None, 3, 4, None, None, 4]}},
        {"in": {"root": _serialize({k: tuple(v) for k, v in fib_ok.items()})}},
        {"in": {"root": _serialize({k: tuple(v) for k, v in fib_bad.items()})}},
        {"in": {"root": list(range(1, 64))}},
        {"in": {"root": [-1, -1, -1, None, None, -1, -1, None, None, -1, None, -1]}},
        {"in": {"root": [((i * 31) % 20001) - 10000 for i in range(2047)]}},
        {"in": {"root": _serialize({k: tuple(v) for k, v in almost_bal.items()})}},
    ]
