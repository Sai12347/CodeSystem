import solution


class Node:
    def __init__(self, x: int, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


if not hasattr(solution, "Node"):
    solution.Node = Node


def run(inp):
    NodeCls = solution.Node
    spec = inp["head"]
    n = len(spec)
    orig = [NodeCls(int(pair[0])) for pair in spec]
    for i in range(n - 1):
        orig[i].next = orig[i + 1]
    for i, pair in enumerate(spec):
        ridx = pair[1]
        orig[i].random = orig[int(ridx)] if ridx is not None else None

    orig_head = orig[0] if n > 0 else None
    orig_ids = {id(node) for node in orig}

    ans = solution.Solution().copyRandomList(orig_head)

    # Verify original list was not corrupted
    cur = orig_head
    for i in range(n):
        expected_rand = orig[int(spec[i][1])] if spec[i][1] is not None else None
        if cur is not orig[i] or cur.val != int(spec[i][0]) or cur.random is not expected_rand:
            return "ERROR: original linked list was modified"
        cur = cur.next
    if cur is not None:
        return "ERROR: original linked list length was modified"

    # Walk and validate copied list
    copied = []
    copy_idx = {}
    cur = ans
    while cur is not None:
        cid = id(cur)
        if cid in orig_ids:
            return "ERROR: returned list shares a node reference with the original list"
        if cid in copy_idx:
            return "ERROR: returned list contains a cycle"
        if len(copied) > n:
            return "ERROR: returned list is longer than input"
        copy_idx[cid] = len(copied)
        copied.append(cur)
        cur = cur.next

    out = []
    for node in copied:
        if node.random is None:
            ridx = None
        else:
            rid = id(node.random)
            if rid not in copy_idx:
                return "ERROR: random pointer does not point to a node in the copied list"
            ridx = copy_idx[rid]
        out.append([int(node.val), ridx])
    return out
