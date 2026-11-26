class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def is_same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if a is None and b is None:
                return True
            if a is None or b is None or a.val != b.val:
                return False
            return is_same(a.left, b.left) and is_same(a.right, b.right)

        if root is None:
            return False
        if is_same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
