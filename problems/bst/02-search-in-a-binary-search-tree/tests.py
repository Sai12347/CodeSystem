from collections import deque


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
        {"in": {"root": [4, 2, 7, 1, 3], "val": 2}},
        {"in": {"root": [4, 2, 7, 1, 3], "val": 5}},
        {"in": {"root": [10, 5, 15, 2, 7, None, 20], "val": 15}},
    ]


def hidden():
    evens = [2 * i for i in range(-1023, 1024)]
    large_bst = _build_balanced_array(evens)
    skew = _skewed_left(list(range(150, 0, -1)))

    return [
        {"in": {"root": [42], "val": 42}},
        {"in": {"root": [42], "val": 7}},
        {"in": {"root": [8, 3, 10, 1, 6, None, 14], "val": 8}},
        {"in": {"root": [8, 3, 10, 1, 6, None, 14], "val": 1}},
        {"in": {"root": [8, 3, 10, 1, 6, None, 14], "val": 14}},
        {"in": {"root": [8, 3, 10, 1, 6], "val": -100}},
        {"in": {"root": [8, 3, 10, 1, 6], "val": 100}},
        {"in": {"root": [-10, -20, -5, -30, -15, -8, -1], "val": -15}},
        {"in": {"root": skew, "val": 1}},
        {"in": {"root": skew, "val": 0}},
        {"in": {"root": large_bst, "val": 1024}},
        {"in": {"root": large_bst, "val": 1025}},
    ]
