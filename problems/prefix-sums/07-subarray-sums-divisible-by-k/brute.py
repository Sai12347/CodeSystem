class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            total = 0
            for j in range(i, n):
                total += nums[j]
                if total % k == 0:
                    ans += 1
        return ans
