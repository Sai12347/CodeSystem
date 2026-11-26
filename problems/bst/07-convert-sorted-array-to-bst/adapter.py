import solution
from judge_lib import TreeNode


def run(inp):
    orig = [int(v) for v in inp["nums"]]
    n = len(orig)
    root = solution.Solution().sortedArrayToBST(list(orig))
    if root is None:
        return "Expected a non-empty TreeNode, got None"
    if not isinstance(root, TreeNode):
        return f"Expected TreeNode, got {type(root).__name__}"

    visited = set()
    inorder = []
    err = [None]

    def dfs(node):
        if node is None or err[0] is not None:
            return 0
        nid = id(node)
        if nid in visited:
            err[0] = "Returned tree contains a cycle or shared node reference"
            return 0
        visited.add(nid)
        if len(visited) > n:
            err[0] = f"Returned tree has more than {n} nodes"
            return 0
        lh = dfs(node.left)
        if err[0] is not None:
            return 0
        inorder.append(node.val)
        rh = dfs(node.right)
        if err[0] is not None:
            return 0
        if abs(lh - rh) > 1:
            err[0] = f"Tree is not height-balanced at node {node.val} (left height {lh}, right height {rh})"
            return 0
        return 1 + max(lh, rh)

    dfs(root)
    if err[0] is not None:
        return err[0]
    if len(inorder) != n:
        return f"Expected {n} nodes, got {len(inorder)}"
    if inorder != orig:
        return "Inorder traversal does not match sorted input array (not a valid BST of nums)"
    return True
