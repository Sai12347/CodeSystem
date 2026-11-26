import solution


class Node:
    def __init__(self, val: int = 0, left=None, right=None, next=None):
        self.val = int(val)
        self.left = left
        self.right = right
        self.next = next


if not hasattr(solution, "Node"):
    solution.Node = Node


def run(inp):
    NodeCls = solution.Node
    vals = inp["root"]
    n = len(vals)
    nodes = [NodeCls(int(v)) for v in vals]
    for i in range(n):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]

    orig_root = nodes[0] if n > 0 else None
    ans = solution.Solution().connect(orig_root)

    if n == 0:
        if ans is not None:
            return "ERROR: expected None for empty tree"
        return []
    if ans is not orig_root:
        return "ERROR: must return the original root node"

    # Verify tree structure and values were not modified
    for i in range(n):
        exp_left = nodes[2 * i + 1] if 2 * i + 1 < n else None
        exp_right = nodes[2 * i + 2] if 2 * i + 2 < n else None
        if nodes[i].val != int(vals[i]) or nodes[i].left is not exp_left or nodes[i].right is not exp_right:
            return "ERROR: tree node values or left/right pointers were modified"

    valid_ids = {id(nd) for nd in nodes}
    out = []
    level = ans
    while level is not None:
        cur = level
        seen = set()
        while cur is not None:
            cid = id(cur)
            if cid not in valid_ids:
                return "ERROR: next pointer points outside the original tree"
            if cid in seen:
                return "ERROR: cycle detected in next pointers"
            seen.add(cid)
            out.append(int(cur.val))
            cur = cur.next
        out.append("#")
        level = level.left
    return out
