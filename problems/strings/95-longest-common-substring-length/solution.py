class Solution:
    def longestCommonSubstring(self, s1: str, s2: str) -> int:
        m = len(s2)
        dp = [0] * (m + 1)
        best = 0
        for ch in s1:
            for j in range(m, 0, -1):
                if ch == s2[j - 1]:
                    dp[j] = dp[j - 1] + 1
                    if dp[j] > best:
                        best = dp[j]
                else:
                    dp[j] = 0
        return best
