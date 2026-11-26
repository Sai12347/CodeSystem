class Solution:
    def totalSubarrayXor(self, nums: List[int]) -> int:
        n = len(nums)
        if n % 2 == 0:
            return 0
        ans = 0
        for i in range(0, n, 2):
            ans ^= nums[i]
        return ans
