class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            zeros = 0
            for j in range(i, n):
                if nums[j] == 0:
                    zeros += 1
                    if zeros > k:
                        break
                if j - i + 1 > best:
                    best = j - i + 1
        return best
