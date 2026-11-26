class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total=sum(nums)
        if total%2: return False
        target=total//2; dp={0}
        for x in nums: dp |= {s+x for s in list(dp) if s+x<=target}
        return target in dp
