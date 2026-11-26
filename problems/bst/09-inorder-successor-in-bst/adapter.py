import solution
from judge_lib import TreeNode, build_tree


def run(inp):
    root = build_tree(inp["root"])
    target_val = int(inp["p"])
    orig_vals = {}
    p_node = None

    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        orig_vals[id(node)] = node.val
        if node.val == target_val:
            p_node = node
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)

    if p_node is None:
        raise ValueError(f"Target node p={target_val} not found in tree")

    res = solution.Solution().inorderSuccessor(root, p_node)
    if res is None:
        return None
    if not isinstance(res, TreeNode):
        return f"Expected TreeNode or None, got {type(res).__name__}"
    if id(res) not in orig_vals:
        return "Returned TreeNode is not a node in the original tree"
    if res.val != orig_vals[id(res)]:
        return "Tree node values must not be modified"
    return int(orig_vals[id(res)])
