class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        best=[0]
        def dfs(n):
            if not n:return (-1,-1)
            l=dfs(n.left);r=dfs(n.right)
            left=1+l[1];right=1+r[0]
            best[0]=max(best[0],left,right)
            return left,right
        dfs(root);return best[0]
