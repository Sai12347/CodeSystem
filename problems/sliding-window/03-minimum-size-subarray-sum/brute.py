class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        best = n + 1
        for i in range(n):
            total = 0
            limit = min(n, i + best - 1)
            for j in range(i, limit):
                total += nums[j]
                if total >= target:
                    best = j - i + 1
                    break
        return 0 if best > n else best
