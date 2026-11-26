from collections import deque
import random


def _build_balanced_array(sorted_vals):
    class _N:
        __slots__ = ("v", "l", "r")
        def __init__(self, v, l=None, r=None):
            self.v = v
            self.l = l
            self.r = r

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return _N(sorted_vals[mid], build(lo, mid - 1), build(mid + 1, hi))

    root = build(0, len(sorted_vals) - 1)
    return _tree_to_arr(root)


def _tree_to_arr(root):
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None)
            continue
        out.append(n.v)
        q.append(n.l)
        q.append(n.r)
    while out and out[-1] is None:
        out.pop()
    return out


def _build_random_bst(vals):
    class _N:
        __slots__ = ("v", "l", "r")
        def __init__(self, v):
            self.v = v
            self.l = None
            self.r = None

    root = None
    for v in vals:
        if root is None:
            root = _N(v)
            continue
        cur = root
        while True:
            if v < cur.v:
                if cur.l is None:
                    cur.l = _N(v)
                    break
                cur = cur.l
            else:
                if cur.r is None:
                    cur.r = _N(v)
                    break
                cur = cur.r
    return _tree_to_arr(root)


def _skewed_right(vals):
    out = [vals[0]]
    for v in vals[1:]:
        out.append(None)
        out.append(v)
    return out


def _skewed_left(vals):
    out = [vals[0]]
    for v in vals[1:]:
        out.append(v)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def visible():
    return [
        {"in": {"root": [4, 2, 7, 1, 3], "val": 5}},
        {"in": {"root": [40, 20, 60, 10, 30, 50, 70], "val": 25}},
        {"in": {"root": [], "val": 5}},
    ]


def hidden():
    rng = random.Random(701)
    rand_vals = rng.sample(range(-100000, 100000), 1501)
    rand_bst = _build_random_bst(rand_vals[:-1])
    rand_insert = rand_vals[-1]

    evens = [2 * i for i in range(-1023, 1024)]
    large_bst = _build_balanced_array(evens)

    return [
        {"in": {"root": [10], "val": 5}},
        {"in": {"root": [10], "val": 15}},
        {"in": {"root": [4, 2, 7, 1, 3], "val": -100000000}},
        {"in": {"root": [4, 2, 7, 1, 3], "val": 100000000}},
        {"in": {"root": [-10, -20, -5, -30, -15, -8, -1], "val": 0}},
        {"in": {"root": [-10, -20, -5, -30, -15, -8, -1], "val": -7}},
        {"in": {"root": _skewed_right(list(range(1, 101))), "val": 101}},
        {"in": {"root": _skewed_left(list(range(100, 0, -1))), "val": 0}},
        {"in": {"root": large_bst, "val": 1}},
        {"in": {"root": rand_bst, "val": rand_insert}},
    ]
