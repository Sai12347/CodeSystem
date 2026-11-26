class Solution:
    def cutRod(self, prices: List[int], n: int) -> int:
        dp=[0]*(n+1)
        for length in range(1,n+1):
            for piece in range(1,length+1): dp[length]=max(dp[length],prices[piece-1]+dp[length-piece])
        return dp[n]
