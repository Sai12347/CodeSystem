class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if root is None:
            return TreeNode(val)
        cur = root
        while True:
            if val < cur.val:
                if cur.left is None:
                    cur.left = TreeNode(val)
                    return root
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = TreeNode(val)
                    return root
                cur = cur.right
