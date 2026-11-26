class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        dp = [i - 1 for i in range(n + 1)]
        for center in range(n):
            l = r = center
            while l >= 0 and r < n and s[l] == s[r]:
                if dp[l] + 1 < dp[r + 1]:
                    dp[r + 1] = dp[l] + 1
                l -= 1
                r += 1
            l, r = center, center + 1
            while l >= 0 and r < n and s[l] == s[r]:
                if dp[l] + 1 < dp[r + 1]:
                    dp[r + 1] = dp[l] + 1
                l -= 1
                r += 1
        return dp[n]
