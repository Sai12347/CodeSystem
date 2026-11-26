class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        a = sorted(nums)
        for i in range(len(a) - 1, 1, -1):
            if a[i - 2] + a[i - 1] > a[i]: return a[i - 2] + a[i - 1] + a[i]
        return 0
