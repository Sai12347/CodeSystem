from collections import deque
import random


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


def _balanced_bst(sorted_vals):
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return [sorted_vals[mid], build(lo, mid - 1), build(mid + 1, hi)]

    return _to_level_order(build(0, len(sorted_vals) - 1))


def _swap_vals(arr, a, b):
    res = list(arr)
    ia = res.index(a)
    ib = res.index(b)
    res[ia], res[ib] = res[ib], res[ia]
    return res


def visible():
    return [
        {"in": {"root": [1, 3, None, None, 2]}},
        {"in": {"root": [3, 1, 4, None, None, 2]}},
        {"in": {"root": [2, 3, 1]}},
    ]


def hidden():
    left_skew = _swap_vals(_insert_bst(list(range(10, 0, -1))), 1, 10)
    right_skew = _swap_vals(_insert_bst(list(range(1, 11))), 5, 6)
    bal15 = _balanced_bst(list(range(1, 16)))

    rng1 = random.Random(991)
    med_vals = rng1.sample(range(-100000, 100001), 300)
    med_sorted = sorted(med_vals)
    med_tree = _swap_vals(_insert_bst(med_vals), med_sorted[40], med_sorted[260])

    rng2 = random.Random(992)
    large_vals = sorted(rng2.sample(range(-1000000, 1000001), 1000))
    large_tree = _swap_vals(_balanced_bst(large_vals), large_vals[499], large_vals[500])

    return [
        {"in": {"root": [1, 2]}},
        {"in": {"root": [2, None, 1]}},
        {"in": {"root": [0, 2147483647, -2147483648]}},
        {"in": {"root": left_skew}},
        {"in": {"root": right_skew}},
        {"in": {"root": _swap_vals(bal15, 8, 1)}},
        {"in": {"root": _swap_vals(bal15, 8, 15)}},
        {"in": {"root": _swap_vals(bal15, 7, 8)}},
        {"in": {"root": med_tree}},
        {"in": {"root": large_tree}},
    ]
