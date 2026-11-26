class Solution:
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            odds = 0
            for j in range(i, n):
                odds += nums[j] & 1
                if odds == k:
                    ans += 1
                elif odds > k:
                    break
        return ans
