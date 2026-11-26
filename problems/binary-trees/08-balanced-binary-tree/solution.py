class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def check(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            lh = check(node.left)
            if lh == -1:
                return -1
            rh = check(node.right)
            if rh == -1 or abs(lh - rh) > 1:
                return -1
            return 1 + (lh if lh > rh else rh)

        return check(root) != -1
