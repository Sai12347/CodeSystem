class Solution:
    def maxAdjacentDiff(self, nums: List[int]) -> int:
        return max((abs(nums[i]-nums[i-1]) for i in range(1,len(nums))), default=0)
