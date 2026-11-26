class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        dp=[0]*(len(text2)+1)
        for a in text1:
            prev=0
            for j,b in enumerate(text2,1):
                old=dp[j]
                dp[j]=prev+1 if a==b else max(dp[j],dp[j-1])
                prev=old
        return dp[-1]
