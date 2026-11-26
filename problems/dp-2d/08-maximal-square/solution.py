class Solution:
    def maximalSquare(self, matrix: List[List[int]]) -> int:
        cols=len(matrix[0]); dp=[0]*(cols+1); best=0
        for row in matrix:
            prev=0
            for j in range(1,cols+1):
                old=dp[j]
                dp[j]=1+min(dp[j],dp[j-1],prev) if row[j-1] else 0
                best=max(best,dp[j]); prev=old
        return best*best
