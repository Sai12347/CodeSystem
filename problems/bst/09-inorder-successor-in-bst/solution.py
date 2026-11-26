class Solution:
    def inorderSuccessor(self, root: Optional[TreeNode], p: Optional[TreeNode]) -> Optional[TreeNode]:
        succ = None
        curr = root
        while curr is not None:
            if p.val < curr.val:
                succ = curr
                curr = curr.left
            else:
                curr = curr.right
        return succ
