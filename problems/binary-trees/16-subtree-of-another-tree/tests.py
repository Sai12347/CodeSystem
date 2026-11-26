import random


def _skewed_ones(n: int, tail_val: int):
    out = [1]
    for i in range(1, n):
        v = tail_val if i == n - 1 else 1
        out.extend([v, None])
    while out and out[-1] is None:
        out.pop()
    return out


def _extract_complete_subtree(arr, idx):
    # Extract level-order subtree rooted at 0-based index idx in a complete tree array
    out = []
    q = [idx]
    for u in q:
        if u < len(arr):
            out.append(arr[u])
            q.append(2 * u + 1)
            q.append(2 * u + 2)
    return out


def visible():
    return [
        {"in": {"root": [3, 4, 5, 1, 2], "subRoot": [4, 1, 2]}},
        {"in": {"root": [3, 4, 5, 1, 2, None, None, None, None, 0], "subRoot": [4, 1, 2]}},
        {"in": {"root": [1], "subRoot": [1]}},
    ]


def hidden():
    rng = random.Random(5721)
    comp_1500 = [rng.randint(-10000, 10000) for _ in range(1500)]
    # Subtree rooted at index 5 in 1500-node complete tree (~220 nodes)
    sub_match = _extract_complete_subtree(comp_1500, 5)

    # Worst-case repetitive tree of 1800 ones with a 500-node subRoot differing only at last node
    comp_1800_ones = [1] * 1800
    sub_mismatch = [1] * 500
    sub_mismatch[-1] = 2

    return [
        # Single nodes with different values
        {"in": {"root": [1], "subRoot": [2]}},
        # subRoot strictly larger than root
        {"in": {"root": [1, 2], "subRoot": [1, 2, 3]}},
        # Exact identical multi-node trees
        {"in": {"root": [5, -3, 8, None, 0, 7, 9], "subRoot": [5, -3, 8, None, 0, 7, 9]}},
        # Duplicate values where root itself doesn't match but child does
        {"in": {"root": [1, 1], "subRoot": [1]}},
        # String-serialization trap: [12] vs [2]
        {"in": {"root": [12], "subRoot": [2]}},
        # Mirror mismatch: left child vs right child
        {"in": {"root": [1, 2, None], "subRoot": [1, None, 2]}},
        # Negative values with multiple decoy subtrees matching top nodes
        {"in": {"root": [-10000, -10000, -10000, 5, 6, 5, 7, None, None, None, None, 1, 2], "subRoot": [-10000, 5, 7, 1, 2]}},
        # Skewed all-1s chain where naive O(n*m) degrades (false)
        {"in": {"root": _skewed_ones(120, 1), "subRoot": _skewed_ones(60, 2)}},
        # Stress 1: 1500-node complete tree with true ~220-node subtree
        {"in": {"root": comp_1500, "subRoot": sub_match}},
        # Stress 2: 1800-node all-1s complete tree with 500-node near-match (false)
        {"in": {"root": comp_1800_ones, "subRoot": sub_mismatch}},
    ]
