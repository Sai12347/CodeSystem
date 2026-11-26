class Solution:
    def minOperationsToMakeContinuous(self, nums: List[int]) -> int:
        n = len(nums)
        a = sorted(set(nums))
        best = left = 0
        for right, x in enumerate(a):
            while x - a[left] >= n: left += 1
            best = max(best, right - left + 1)
        return n - best
