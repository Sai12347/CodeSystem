class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i, v in enumerate(nums):
            prefix[i + 1] = prefix[i] + v
        best = n + 1
        for i in range(n):
            pi = prefix[i]
            limit = min(n + 1, i + best)
            for j in range(i + 1, limit):
                if prefix[j] - pi >= k:
                    best = j - i
                    break
        return best if best <= n else -1
