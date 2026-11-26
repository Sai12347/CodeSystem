class Solution:
    def getMaximumXor(self, nums: List[int], maximumBit: int) -> List[int]:
        mask = (1 << maximumBit) - 1
        cur = 0
        for v in nums:
            cur ^= v
        n = len(nums)
        ans = [0] * n
        for i in range(n):
            ans[i] = cur ^ mask
            cur ^= nums[n - 1 - i]
        return ans
