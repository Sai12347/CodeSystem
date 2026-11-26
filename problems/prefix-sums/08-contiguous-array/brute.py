class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            zeros = 0
            ones = 0
            for j in range(i, n):
                if nums[j] == 0:
                    zeros += 1
                else:
                    ones += 1
                if zeros == ones and (j - i + 1) > best:
                    best = j - i + 1
        return best
