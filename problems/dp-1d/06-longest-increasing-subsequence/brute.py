class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # Independent O(n^2) DP verification
        n = len(nums)
        dp = [1] * n
        for i in range(n):
            ni = nums[i]
            best = 1
            for j in range(i):
                if nums[j] < ni and dp[j] + 1 > best:
                    best = dp[j] + 1
            dp[i] = best
        return max(dp)
