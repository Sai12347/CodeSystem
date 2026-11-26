class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        res = [0] * len(nums)
        total = 0
        for i, x in enumerate(nums):
            total += x
            res[i] = total
        return res
