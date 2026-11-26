class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        half=sum(stones)//2; dp={0}
        for x in stones: dp |= {s+x for s in list(dp) if s+x<=half}
        return sum(stones)-2*max(dp)
