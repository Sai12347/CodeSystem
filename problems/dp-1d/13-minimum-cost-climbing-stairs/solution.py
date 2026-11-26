class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        a=b=0
        for x in cost:a,b=b,min(a+x,b+x)
        return min(a,b)
