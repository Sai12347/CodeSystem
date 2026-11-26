class Solution:
    def maxKSumPairs(self, nums: List[int], k: int) -> int:
        a = sorted(nums)
        i, j, pairs = 0, len(a) - 1, 0
        while i < j:
            total = a[i] + a[j]
            if total == k: pairs += 1; i += 1; j -= 1
            elif total < k: i += 1
            else: j -= 1
        return pairs
