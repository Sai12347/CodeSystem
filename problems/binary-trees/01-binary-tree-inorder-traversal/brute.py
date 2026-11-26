class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res: List[int] = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)

        dfs(root)
        return res
