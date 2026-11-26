class Solution:
    def maximumAdjacentProduct(self, nums: List[int]) -> int:
        best = nums[0] * nums[1]
        for i in range(1, len(nums) - 1):
            best = max(best, nums[i] * nums[i + 1])
        return best
