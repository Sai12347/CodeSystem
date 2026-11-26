import solution


class Node:
    def __init__(self, val: int = 0, prev=None, next=None, child=None):
        self.val = int(val)
        self.prev = prev
        self.next = next
        self.child = child


if not hasattr(solution, "Node"):
    solution.Node = Node


def _build_level(items, NodeCls, counter):
    head = None
    tail = None
    for item in items:
        if isinstance(item, list):
            if tail is None:
                raise ValueError("Child list without preceding node")
            tail.child = _build_level(item, NodeCls, counter)
        else:
            node = NodeCls(int(item))
            counter[0] += 1
            if head is None:
                head = node
                tail = node
            else:
                tail.next = node
                node.prev = tail
                tail = node
    return head


def run(inp):
    NodeCls = solution.Node
    spec = inp["head"]
    counter = [0]
    root = _build_level(spec, NodeCls, counter) if spec else None
    total = counter[0]

    ans = solution.Solution().flatten(root)

    if total == 0:
        if ans is not None:
            return "ERROR: expected null for empty input"
        return []
    if ans is None:
        return []
    if ans.prev is not None:
        return "ERROR: head.prev must be null"

    out = []
    seen = set()
    cur = ans
    while cur is not None:
        cid = id(cur)
        if cid in seen:
            return "ERROR: returned list contains a cycle"
        seen.add(cid)
        if cur.child is not None:
            return f"ERROR: node {cur.val} still has a non-null child pointer"
        if cur.next is not None and cur.next.prev is not cur:
            return f"ERROR: broken prev pointer after node {cur.val}"
        out.append(int(cur.val))
        if len(out) > total:
            return "ERROR: returned list has more nodes than input"
        cur = cur.next

    if len(out) != total:
        return f"ERROR: expected {total} nodes, got {len(out)}"
    return out
