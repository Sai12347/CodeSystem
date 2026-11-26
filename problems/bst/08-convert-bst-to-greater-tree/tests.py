from collections import deque
import random


def _serialize_bst_from_balanced(vals):
    if not vals:
        return []
    n = len(vals)

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return [vals[mid], build(lo, mid - 1), build(mid + 1, hi)]

    return _to_level_order(build(0, n - 1))


def _insert_bst(vals):
    root = None
    for v in vals:
        if root is None:
            root = [v, None, None]
            continue
        cur = root
        while True:
            if v < cur[0]:
                if cur[1] is None:
                    cur[1] = [v, None, None]
                    break
                cur = cur[1]
            else:
                if cur[2] is None:
                    cur[2] = [v, None, None]
                    break
                cur = cur[2]
    return _to_level_order(root)


def _to_level_order(root):
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node[0])
            q.append(node[1])
            q.append(node[2])
    while out and out[-1] is None:
        out.pop()
    return out


def visible():
    return [
        {"in": {"root": [4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8]}},
        {"in": {"root": [0, None, 1]}},
        {"in": {"root": [3, 2, 4, 1]}},
    ]


def hidden():
    rng1 = random.Random(5381)
    med_vals = rng1.sample(range(-10000, 10001), 300)
    med_tree = _insert_bst(med_vals)

    rng2 = random.Random(5382)
    large_vals = sorted(rng2.sample(range(-10000, 10001), 2000))
    large_tree = _serialize_bst_from_balanced(large_vals)

    left_skew = _insert_bst(list(range(10, 0, -1)))
    right_skew = _insert_bst(list(range(1, 11)))
    zigzag = _insert_bst([10, 1, 9, 2, 8, 3, 7, 4, 6, 5])

    return [
        {"in": {"root": []}},
        {"in": {"root": [42]}},
        {"in": {"root": [-10000]}},
        {"in": {"root": [-5, -10, -2, -15, -7, -3, -1]}},
        {"in": {"root": left_skew}},
        {"in": {"root": right_skew}},
        {"in": {"root": zigzag}},
        {"in": {"root": [0, -10000, 10000]}},
        {"in": {"root": med_tree}},
        {"in": {"root": large_tree}},
    ]
