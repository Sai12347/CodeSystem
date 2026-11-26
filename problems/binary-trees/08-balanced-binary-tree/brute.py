class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))

        def ok(node: Optional[TreeNode]) -> bool:
            if not node:
                return True
            if abs(height(node.left) - height(node.right)) > 1:
                return False
            return ok(node.left) and ok(node.right)

        return ok(root)
