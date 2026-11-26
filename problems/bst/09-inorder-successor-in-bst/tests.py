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


def visible():
    return [
        {"in": {"root": [2, 1, 3], "p": 1}},
        {"in": {"root": [5, 3, 6, 2, 4, None, None, 1], "p": 6}},
        {"in": {"root": [5, 3, 6, 2, 4, None, None, 1], "p": 4}},
    ]


def hidden():
    left_skew = _insert_bst(list(range(10, 0, -1)))
    right_skew = _insert_bst(list(range(1, 11)))
    deep_right_left = _insert_bst([20, 10, 30, 5, 15, 25, 35, 22, 21])
    neg_ext = _insert_bst([0, -100000, 100000, -50000, 50000, -1, 1])
    deep_ancestor = _insert_bst([50, 20, 80, 10, 30, 25, 40, 35, 45, 48])

    rng1 = random.Random(2851)
    med_vals = rng1.sample(range(-100000, 100001), 500)
    med_tree = _insert_bst(med_vals)
    med_target = sorted(med_vals)[249]

    rng2 = random.Random(2852)
    large_vals = sorted(rng2.sample(range(-100000, 100001), 3000))
    large_tree = _balanced_bst(large_vals)
    large_target = large_vals[(len(large_vals) - 1) // 2]

    return [
        {"in": {"root": [1], "p": 1}},
        {"in": {"root": deep_right_left, "p": 20}},
        {"in": {"root": left_skew, "p": 1}},
        {"in": {"root": left_skew, "p": 10}},
        {"in": {"root": right_skew, "p": 1}},
        {"in": {"root": right_skew, "p": 10}},
        {"in": {"root": neg_ext, "p": -1}},
        {"in": {"root": deep_ancestor, "p": 48}},
        {"in": {"root": med_tree, "p": med_target}},
        {"in": {"root": large_tree, "p": large_target}},
    ]
