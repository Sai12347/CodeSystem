class Solution:
    def prefixesDivBy5(self, nums: List[int]) -> List[bool]:
        ans = [False] * len(nums)
        rem = 0
        for i, bit in enumerate(nums):
            rem = ((rem << 1) | bit) % 5
            ans[i] = rem == 0
        return ans
