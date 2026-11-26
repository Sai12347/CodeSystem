class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        window_sum = 0
        best = len(nums) + 1
        for right, val in enumerate(nums):
            window_sum += val
            while window_sum >= target:
                length = right - left + 1
                if length < best:
                    best = length
                window_sum -= nums[left]
                left += 1
        return 0 if best > len(nums) else best
