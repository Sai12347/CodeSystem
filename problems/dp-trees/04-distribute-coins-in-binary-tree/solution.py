class Solution:
    def distributeCoins(self, root: Optional[TreeNode]) -> int:
        moves=0
        def dfs(n):
            nonlocal moves
            if not n:return 0
            l=dfs(n.left);r=dfs(n.right)
            moves+=abs(l)+abs(r)
            return n.val+l+r-1
        dfs(root);return moves
