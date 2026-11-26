class Solution:
    def minimumEqualDistance(self, nums: List[int]) -> int:
        last = {}
        best = len(nums) + 1
        for i, x in enumerate(nums):
            if x in last:
                best = min(best, i - last[x])
            last[x] = i
        return best if best <= len(nums) else -1
