class Solution:
    def differenceOfSumAndDigitSum(self, nums: List[int]) -> int:
        element_sum = sum(nums)
        digit_sum = sum(sum(map(int, str(x))) for x in nums)
        return abs(element_sum - digit_sum)
