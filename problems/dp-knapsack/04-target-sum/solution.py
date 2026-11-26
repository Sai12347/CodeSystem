class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp={0:1}
        for x in nums:
            nxt={}
            for s,count in dp.items():
                nxt[s+x]=nxt.get(s+x,0)+count
                nxt[s-x]=nxt.get(s-x,0)+count
            dp=nxt
        return dp.get(target,0)
