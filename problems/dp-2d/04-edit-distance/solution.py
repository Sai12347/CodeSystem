class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        dp=list(range(len(word2)+1))
        for i,a in enumerate(word1,1):
            prev=dp[0]; dp[0]=i
            for j,b in enumerate(word2,1):
                old=dp[j]
                dp[j]=prev if a==b else 1+min(prev,dp[j],dp[j-1])
                prev=old
        return dp[-1]
