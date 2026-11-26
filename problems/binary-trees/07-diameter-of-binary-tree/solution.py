class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0

        def height(node: Optional[TreeNode]) -> int:
            nonlocal best
            if not node:
                return 0
            lh = height(node.left)
            rh = height(node.right)
            if lh + rh > best:
                best = lh + rh
            return 1 + (lh if lh > rh else rh)

        height(root)
        return best
