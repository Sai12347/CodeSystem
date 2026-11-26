class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        # states: 0 needs camera, 1 covered, 2 has camera
        cams=0
        def dfs(n):
            nonlocal cams
            if not n:return 1
            l=dfs(n.left);r=dfs(n.right)
            if l==0 or r==0:cams+=1;return 2
            if l==2 or r==2:return 1
            return 0
        if dfs(root)==0:cams+=1
        return cams
