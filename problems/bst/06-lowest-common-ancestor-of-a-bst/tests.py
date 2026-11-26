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


def _skewed_left(vals):
    out = [vals[0]]
    for v in vals[1:]:
        out.append(v)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def _skewed_right(vals):
    out = [vals[0]]
    for v in vals[1:]:
        out.append(None)
        out.append(v)
    return out


def visible():
    return [
        {"in": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 8}},
        {"in": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 4}},
        {"in": {"root": [2, 1], "p": 2, "q": 1}},
    ]


def hidden():
    rng = random.Random(235)
    rand_vals = rng.sample(range(-1000000000, 1000000001), 1500)
    rand_bst = _build_random_bst(rand_vals)

    large_bst = _build_balanced_array(list(range(-1023, 1024)))
    deep_right = _build_random_bst([20, 10, 30, 25, 40, 22, 28, 35, 50])

    return [
        {"in": {"root": [1, None, 2], "p": 2, "q": 1}},
        {"in": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 3, "q": 5}},
        {"in": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 9, "q": 0}},
        {"in": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 5, "q": 2}},
        {"in": {"root": [0, -1000000000, 1000000000, None, -500000000, 500000000, None], "p": -1000000000, "q": -500000000}},
        {"in": {"root": _skewed_left(list(range(100, 0, -1))), "p": 1, "q": 40}},
        {"in": {"root": _skewed_right(list(range(1, 101))), "p": 75, "q": 99}},
        {"in": {"root": deep_right, "p": 35, "q": 50}},
        {"in": {"root": large_bst, "p": 513, "q": 1023}},
        {"in": {"root": rand_bst, "p": rand_vals[900], "q": rand_vals[1499]}},
    ]
