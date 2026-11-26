class Solution:
    def longestIncreasingRun(self, nums: List[int]) -> int:
        best = run = 1
        for i in range(1, len(nums)):
            run = run + 1 if nums[i] > nums[i - 1] else 1
            best = max(best, run)
        return best
