from collections import deque


def _build_balanced_array(sorted_vals):
    if not sorted_vals:
        return []

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


def _skewed_right(vals):
    if not vals:
        return []
    out = [vals[0]]
    for v in vals[1:]:
        out.append(None)
        out.append(v)
    return out


def _skewed_left(vals):
    if not vals:
        return []
    out = [vals[0]]
    for v in vals[1:]:
        out.append(v)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def visible():
    return [
        {"in": {"root": [2, 1, 3]}},
        {"in": {"root": [5, 1, 4, None, None, 3, 6]}},
        {"in": {"root": [5, 4, 6, None, None, 3, 7]}},
    ]


def hidden():
    large_valid = _build_balanced_array(list(range(-1023, 1024)))
    large_invalid = list(large_valid)
    # Corrupt a deep node in the right subtree of the root (root is index 0, value 0)
    # Right child of root is index 2; deep left descendant of right subtree should be > 0, set it to -1
    idx = 2
    while 2 * idx + 1 < len(large_invalid):
        idx = 2 * idx + 1
    large_invalid[idx] = -1

    return [
        {"in": {"root": [0]}},
        {"in": {"root": [2, 2, 2]}},
        {"in": {"root": [-2147483648]}},
        {"in": {"root": [2147483647]}},
        {"in": {"root": [-2147483648, None, 2147483647]}},
        {"in": {"root": [-2147483648, -2147483648]}},
        {"in": {"root": [2147483647, None, 2147483647]}},
        {"in": {"root": [10, 5, 15, 3, 12, None, 20]}},
        {"in": {"root": [-10, -20, -5, -30, -15, -8, -1]}},
        {"in": {"root": _skewed_right(list(range(-50, 70)))}},
        {"in": {"root": _skewed_left([50, 40, 30, 20, 20, 10])}},
        {"in": {"root": large_valid}},
        {"in": {"root": large_invalid}},
    ]
