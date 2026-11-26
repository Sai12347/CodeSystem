class Solution:
    def maximumCount(self, nums: List[int]) -> int:
        negative = sum(x < 0 for x in nums)
        positive = sum(x > 0 for x in nums)
        return max(negative, positive)
