class Solution:
    def maxCoveredBitmasks(self, masks: List[int], m: int, k: int) -> int:
        size = 1 << m
        dp = [0] * size
        for x in masks:
            dp[x] += 1
        for b in range(m):
            bit = 1 << b
            step = bit << 1
            for start in range(bit, size, step):
                for mask in range(start, start + bit):
                    dp[mask] += dp[mask ^ bit]
        ans = 0
        for s in range(size):
            if s.bit_count() == k and dp[s] > ans:
                ans = dp[s]
        return ans
