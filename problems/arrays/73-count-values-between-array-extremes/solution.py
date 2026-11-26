class Solution:
    def countBetweenExtremes(self, nums: List[int]) -> int:
        low, high = min(nums), max(nums)
        return sum(low < x < high for x in nums)
