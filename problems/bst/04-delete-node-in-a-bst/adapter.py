from judge_lib import TreeNode, build_tree
import solution


def run(inp):
    raw_root = inp["root"]
    key = int(inp["key"])
    expected = sorted(int(x) for x in raw_root if x is not None and int(x) != key)

    root = build_tree(raw_root)
    res = solution.Solution().deleteNode(root, key)

    if not expected:
        if res is None:
            return True
        return "Expected empty tree (null), got non-empty tree"

    if res is None:
        return f"Expected {len(expected)} nodes, got null"
    if not isinstance(res, TreeNode):
        return f"Expected TreeNode, got {type(res).__name__}"

    seen = set()
    stack = []
    cur = res
    vals = []
    while cur is not None or stack:
        while cur is not None:
            if not isinstance(cur, TreeNode):
                return f"Invalid child type {type(cur).__name__}"
            nid = id(cur)
            if nid in seen:
                return "Cycle or shared node detected in returned tree"
            seen.add(nid)
            if len(seen) > len(expected):
                return f"Returned tree has more than {len(expected)} nodes"
            stack.append(cur)
            cur = cur.left
        node = stack.pop()
        vals.append(int(node.val))
        cur = node.right

    if len(vals) != len(expected):
        return f"Expected {len(expected)} nodes, got {len(vals)}"
    for i in range(1, len(vals)):
        if vals[i] <= vals[i - 1]:
            return "Returned tree is not a valid BST"
    if vals != expected:
        return "Node values do not match expected values after deletion"
    return True
