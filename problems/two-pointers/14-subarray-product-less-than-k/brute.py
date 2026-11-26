class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0
        n = len(nums)
        ans = 0
        for i in range(n):
            prod = 1
            for j in range(i, n):
                prod *= nums[j]
                if prod < k:
                    ans += 1
                else:
                    break
        return ans
