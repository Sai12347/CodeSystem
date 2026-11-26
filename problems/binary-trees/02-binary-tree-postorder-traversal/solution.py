class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res: List[int] = []
        stack: List[TreeNode] = []
        cur = root
        last_visited: Optional[TreeNode] = None
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            peek = stack[-1]
            if peek.right and last_visited is not peek.right:
                cur = peek.right
            else:
                res.append(peek.val)
                last_visited = stack.pop()
        return res
