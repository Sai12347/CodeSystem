class Solution:
    def minPairSum(self, nums: List[int]) -> int:
        a = sorted(nums)
        return max(a[i] + a[-1-i] for i in range(len(a) // 2))
