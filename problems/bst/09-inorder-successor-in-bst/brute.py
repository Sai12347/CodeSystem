class Solution:
    def inorderSuccessor(self, root: Optional[TreeNode], p: Optional[TreeNode]) -> Optional[TreeNode]:
        order = []

        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            dfs(node.left)
            order.append(node)
            dfs(node.right)

        dfs(root)
        for i, node in enumerate(order):
            if node is p:
                return order[i + 1] if i + 1 < len(order) else None
        return None
