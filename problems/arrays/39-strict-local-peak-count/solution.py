class Solution:
    def countStrictPeaks(self, nums: List[int]) -> int:
        return sum(1 for i in range(1, len(nums) - 1) if nums[i] > nums[i - 1] and nums[i] > nums[i + 1])
