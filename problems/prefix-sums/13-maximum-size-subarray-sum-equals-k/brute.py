class Solution:
    def maxSubArrayLen(self, nums: List[int], k: int) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            total = 0
            for j in range(i, n):
                total += nums[j]
                if total == k and (j - i + 1) > best:
                    best = j - i + 1
        return best
