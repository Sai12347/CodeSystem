class Solution:
    def maxCircularSubarraySum(self, nums: List[int]) -> int:
        total = sum(nums)
        max_end = min_end = max_sum = min_sum = nums[0]
        for x in nums[1:]:
            max_end = max(x, max_end + x)
            max_sum = max(max_sum, max_end)
            min_end = min(x, min_end + x)
            min_sum = min(min_sum, min_end)
        return max_sum if max_sum < 0 else max(max_sum, total - min_sum)
