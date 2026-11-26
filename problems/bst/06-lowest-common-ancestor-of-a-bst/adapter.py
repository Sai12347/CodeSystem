from judge_lib import TreeNode, build_tree
import solution


def run(inp):
    root = build_tree(inp["root"])
    p_val = int(inp["p"])
    q_val = int(inp["q"])

    p_node = None
    q_node = None
    node_ids = set()
    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        node_ids.add(id(node))
        if node.val == p_val:
            p_node = node
        if node.val == q_val:
            q_node = node
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)

    res = solution.Solution().lowestCommonAncestor(root, p_node, q_node)
    if res is None:
        return None
    if not isinstance(res, TreeNode) or id(res) not in node_ids:
        return "Returned node is not a node from the input tree"
    return int(res.val)
