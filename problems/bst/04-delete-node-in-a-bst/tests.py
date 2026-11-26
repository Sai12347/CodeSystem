from collections import deque
import random


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

    return _tree_to_arr(build(0, len(sorted_vals) - 1))


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


def visible():
    return [
        {"in": {"root": [5, 3, 6, 2, 4, None, 7], "key": 3}},
        {"in": {"root": [5, 3, 6, 2, 4, None, 7], "key": 0}},
        {"in": {"root": [], "key": 0}},
    ]


def hidden():
    rng = random.Random(450)
    rand_vals = rng.sample(range(-100000, 100001), 1500)
    rand_bst = _build_random_bst(rand_vals)
    rand_key = rand_vals[5]

    large_bst = _build_balanced_array(list(range(-1023, 1024)))
    # Tree where root's inorder successor (12) is deep left and has a right child (13)
    deep_succ_bst = _build_random_bst([10, 5, 20, 2, 7, 15, 30, 12, 18, 13])

    return [
        {"in": {"root": [5], "key": 5}},
        {"in": {"root": [5], "key": 3}},
        {"in": {"root": [5, 3, 6, 2, 4, None, 7], "key": 5}},
        {"in": {"root": [5, 3, 6, 2, 4, None, 7], "key": 2}},
        {"in": {"root": [5, 3, 6, None, 4, None, 7], "key": 6}},
        {"in": {"root": [5, 3, 6, 2, None], "key": 3}},
        {"in": {"root": [5, 3], "key": 5}},
        {"in": {"root": deep_succ_bst, "key": 10}},
        {"in": {"root": [-10, -20, -5, -30, -15, -8, -1], "key": -10}},
        {"in": {"root": _skewed_right(list(range(1, 101))), "key": 50}},
        {"in": {"root": large_bst, "key": 0}},
        {"in": {"root": rand_bst, "key": rand_key}},
    ]
