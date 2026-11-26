class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return 0
        s = sorted(nums)
        return max(s[i + 1] - s[i] for i in range(len(s) - 1))
