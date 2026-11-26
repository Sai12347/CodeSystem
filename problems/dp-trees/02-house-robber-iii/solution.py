class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dp(n):
            if not n:return (0,0)
            l=dp(n.left);r=dp(n.right)
            take=n.val+l[1]+r[1]
            skip=max(l)+max(r)
            return take,skip
        return max(dp(root))
