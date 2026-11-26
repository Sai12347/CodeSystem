class Solution:
    def countValidSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [0] * n
        stack = []
        total = 0
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            elif stack:
                j = stack.pop()
                dp[i] = 1 + (dp[j - 1] if j > 0 else 0)
                total += dp[i]
        return total
