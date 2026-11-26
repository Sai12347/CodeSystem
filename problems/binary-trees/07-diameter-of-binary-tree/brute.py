class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))

        def solve(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            through = height(node.left) + height(node.right)
            return max(through, solve(node.left), solve(node.right))

        return solve(root)
