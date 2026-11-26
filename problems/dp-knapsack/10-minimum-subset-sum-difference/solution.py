class Solution:
    def minimumDifference(self, nums: List[int]) -> int:
        total=sum(nums);possible={0}
        for x in nums:possible|={s+x for s in tuple(possible) if s+x<=total//2}
        return total-2*max(possible)
