class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        dp=grid[0][:]
        for i in range(1,len(grid)):
            dp[0]+=grid[i][0]
            for j in range(1,len(dp)): dp[j]=min(dp[j],dp[j-1])+grid[i][j]
        return dp[-1]
