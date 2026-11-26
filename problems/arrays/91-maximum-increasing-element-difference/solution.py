class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        low = nums[0]; best = -1
        for x in nums[1:]:
            if x > low: best = max(best, x - low)
            low = min(low, x)
        return best
