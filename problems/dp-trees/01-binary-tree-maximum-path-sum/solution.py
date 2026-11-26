class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best=[-10**9]
        def dfs(node):
            if not node:return 0
            l=max(0,dfs(node.left));r=max(0,dfs(node.right))
            best[0]=max(best[0],node.val+l+r)
            return node.val+max(l,r)
        dfs(root);return best[0]
