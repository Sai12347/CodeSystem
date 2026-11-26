from collections import deque
from judge_lib import build_tree
import solution


def run(inp):
    root = build_tree(inp["root"])
    p_val = int(inp["p"])
    q_val = int(inp["q"])

    p_node = None
    q_node = None
    orig_vals = {}
    if root is not None:
        dq = deque([root])
        while dq:
            node = dq.popleft()
            orig_vals[id(node)] = node.val
            if node.val == p_val:
                p_node = node
            if node.val == q_val:
                q_node = node
            if node.left is not None:
                dq.append(node.left)
            if node.right is not None:
                dq.append(node.right)

    ans = solution.Solution().lowestCommonAncestor(root, p_node, q_node)
    if ans is None or id(ans) not in orig_vals:
        return "ERROR: returned node is null or not a node from the input tree"
    if ans.val != orig_vals[id(ans)]:
        return "ERROR: node value was modified"
    return int(ans.val)
