class Solution:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        mod=10**9+7;d=[[0]*(n+1) for _ in range(minProfit+1)];d[0]=[1]*(n+1)
        for g,p in zip(group,profit):
            for need in range(minProfit,-1,-1):
                for people in range(n,g-1,-1):
                    d[need][people]=(d[need][people]+d[max(0,need-p)][people-g])%mod
        return d[minProfit][n]
