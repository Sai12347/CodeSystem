class Solution:
    def maxSubarraySum(self, nums: List[int], k: int) -> int:
        window_sum = sum(nums[:k])
        best = window_sum
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            if window_sum > best:
                best = window_sum
        return best
