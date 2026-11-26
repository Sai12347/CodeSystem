class Solution:
    def dominantIndex(self, nums: List[int]) -> int:
        best = second = -1
        index = -1
        for i, x in enumerate(nums):
            if x > best:
                second, best, index = best, x, i
            elif x > second:
                second = x
        return index if best >= 2 * second else -1
