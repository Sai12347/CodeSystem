class Solution:
    def longestDisjointSubarray(self, nums: List[int]) -> int:
        used = 0
        left = 0
        best = 0
        for right, x in enumerate(nums):
            while used & x:
                used ^= nums[left]
                left += 1
            used |= x
            cur = right - left + 1
            if cur > best:
                best = cur
        return best
