class Solution:
    def longestArithSeqLength(self, nums: List[int]) -> int:
        dp = [{} for _ in nums]
        best = 2
        for i in range(len(nums)):
            for j in range(i):
                d = nums[i] - nums[j]
                dp[i][d] = dp[j].get(d, 1) + 1
                best = max(best, dp[i][d])
        return best
