class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if root is None:
            return None
        if root.val == val:
            return root
        left = self.searchBST(root.left, val)
        if left is not None:
            return left
        return self.searchBST(root.right, val)
