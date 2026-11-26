class Solution:
    def arraySign(self, nums: List[int]) -> int:
        prod = 1
        for x in nums:
            prod *= x
        if prod > 0:
            return 1
        if prod < 0:
            return -1
        return 0
