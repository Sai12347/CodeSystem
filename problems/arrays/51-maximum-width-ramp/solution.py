class Solution:
    def maxWidthRamp(self, nums: List[int]) -> int:
        candidates = []
        for i, x in enumerate(nums):
            if not candidates or x < nums[candidates[-1]]: candidates.append(i)
        best = 0
        for j in range(len(nums) - 1, -1, -1):
            while candidates and nums[candidates[-1]] <= nums[j]: best = max(best, j - candidates.pop())
        return best
