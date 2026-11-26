class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hold=-10**9;sold=rest=0
        for p in prices:
            hold,sold,rest=max(hold,rest-p),hold+p,sold if sold>rest else rest
        return max(sold,rest)
