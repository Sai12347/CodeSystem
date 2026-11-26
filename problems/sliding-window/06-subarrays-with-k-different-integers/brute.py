class Solution:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(nums[j])
                size = len(seen)
                if size == k:
                    ans += 1
                elif size > k:
                    break
        return ans
