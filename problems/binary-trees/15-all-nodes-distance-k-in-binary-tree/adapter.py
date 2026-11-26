from collections import deque
from judge_lib import build_tree
import solution


def run(inp):
    root = build_tree(inp["root"])
    target_val = int(inp["target"])
    k = int(inp["k"])

    target_node = None
    if root is not None:
        q = deque([root])
        while q:
            node = q.popleft()
            if node.val == target_val:
                target_node = node
                break
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)

    res = solution.Solution().distanceK(root, target_node, k)
    if res is None:
        return "ERROR: expected list of integers, got None"
    return [int(x) for x in res]
