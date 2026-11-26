class Solution:
    def shortestTour(self, costs: List[List[int]]) -> int:
        n=len(costs);full=(1<<n)-1;dp=[[float('inf')]*n for _ in range(1<<n)];dp[1][0]=0
        for mask in range(1<<n):
            if not mask&1:continue
            for u in range(n):
                if dp[mask][u]==float('inf'):continue
                for v in range(n):
                    if not mask>>v&1:dp[mask|1<<v][v]=min(dp[mask|1<<v][v],dp[mask][u]+costs[u][v])
        return min(dp[full][u]+costs[u][0] for u in range(n))
