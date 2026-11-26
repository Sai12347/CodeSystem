class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        prefix = 0
        min_prefix = 0
        best = nums[0]
        for x in nums:
            prefix += x
            if prefix - min_prefix > best:
                best = prefix - min_prefix
            if prefix < min_prefix:
                min_prefix = prefix
        return best
