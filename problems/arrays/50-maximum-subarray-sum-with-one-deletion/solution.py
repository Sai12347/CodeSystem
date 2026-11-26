class Solution:
    def maximumSumWithOneDeletion(self, nums: List[int]) -> int:
        keep = nums[0]
        drop = 0
        best = nums[0]
        for x in nums[1:]:
            drop = max(keep, drop + x)
            keep = max(x, keep + x)
            best = max(best, keep, drop)
        return best
