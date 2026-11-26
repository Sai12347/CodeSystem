class Solution:
    def maxProductOfTwoElements(self, nums: List[int]) -> int:
        first = second = 0
        for x in nums:
            if x > first: first, second = x, first
            elif x > second: second = x
        return first * second
