class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        best = 0
        n = len(nums)
        for i in range(n):
            a = nums[i]
            for j in range(i, n):
                v = a ^ nums[j]
                if v > best:
                    best = v
        return best
