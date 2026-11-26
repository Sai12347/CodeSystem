class Solution:
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [0] * n
        best = nums[0]
        for i in range(n):
            prev = 0
            start = max(0, i - k)
            for j in range(start, i):
                if dp[j] > prev:
                    prev = dp[j]
            dp[i] = nums[i] + prev
            if dp[i] > best:
                best = dp[i]
        return best
