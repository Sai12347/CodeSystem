class Solution:
    def subsetXorSum(self, nums: List[int]) -> int:
        or_all = 0
        for x in nums:
            or_all |= x
        return or_all << (len(nums) - 1)
