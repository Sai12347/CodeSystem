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
        {"in": {"root": [3, 1, 4, None, 2], "k": 1}},
        {"in": {"root": [5, 3, 6, 2, 4, None, None, 1], "k": 3}},
        {"in": {"root": [10, 5, 15, 2, 7, 12, 20], "k": 6}},
    ]


def hidden():
    rng = random.Random(230)
    rand_vals = rng.sample(range(-100000, 100001), 1500)
    rand_bst = _build_random_bst(rand_vals)

    large_bst = _build_balanced_array(list(range(-1023, 1024)))
    left_skew = _skewed_left(list(range(100, 0, -1)))
    right_skew = _skewed_right(list(range(-50, 50)))
    zigzag = _build_random_bst([50, 10, 40, 20, 35, 25, 30])

    return [
        {"in": {"root": [0], "k": 1}},
        {"in": {"root": [5, 3, 6, 2, 4, None, None, 1], "k": 6}},
        {"in": {"root": [-10, -20, -5, -30, -15, -8, -1], "k": 1}},
        {"in": {"root": [0, -5, 5, -10, -2, 2, 10], "k": 4}},
        {"in": {"root": left_skew, "k": 1}},
        {"in": {"root": left_skew, "k": 100}},
        {"in": {"root": right_skew, "k": 50}},
        {"in": {"root": zigzag, "k": 4}},
        {"in": {"root": large_bst, "k": 1}},
        {"in": {"root": rand_bst, "k": 1111}},
    ]
