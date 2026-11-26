class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        def is_mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return is_mirror(a.left, b.right) and is_mirror(a.right, b.left)

        return is_mirror(root.left, root.right)
