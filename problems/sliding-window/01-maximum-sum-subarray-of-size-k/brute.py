class Solution:
    def maxSubarraySum(self, nums: List[int], k: int) -> int:
        return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
