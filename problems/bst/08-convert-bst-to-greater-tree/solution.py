class Solution:
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        running_sum = 0
        curr = root
        while curr is not None:
            if curr.right is None:
                running_sum += curr.val
                curr.val = running_sum
                curr = curr.left
            else:
                succ = curr.right
                while succ.left is not None and succ.left is not curr:
                    succ = succ.left
                if succ.left is None:
                    succ.left = curr
                    curr = curr.right
                else:
                    succ.left = None
                    running_sum += curr.val
                    curr.val = running_sum
                    curr = curr.left
        return root
