class Solution:
    def minSwapsToGroupOnes(self, nums: List[int]) -> int:
        ones = sum(nums)
        if ones <= 1: return 0
        current = sum(nums[:ones])
        best = current
        for right in range(ones, len(nums)):
            current += nums[right] - nums[right - ones]
            best = max(best, current)
        return ones - best
