class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        cur = root
        while cur is not None:
            if cur.val == val:
                return cur
            if val < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        return None
