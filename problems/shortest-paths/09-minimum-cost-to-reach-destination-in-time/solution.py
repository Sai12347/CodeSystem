class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        n=len(passingFees);g=[[] for _ in range(n)]
        for a,b,t in edges:g[a].append((b,t));g[b].append((a,t))
        inf=10**9;best=[[inf]*n for _ in range(maxTime+1)];best[0][0]=passingFees[0];q=[(passingFees[0],0,0)]
        while q:
            cost,t,u=heapq.heappop(q)
            if cost!=best[t][u]:continue
            if u==n-1:return cost
            for v,w in g[u]:
                nt=t+w
                if nt<=maxTime and cost+passingFees[v]<best[nt][v]:best[nt][v]=cost+passingFees[v];heapq.heappush(q,(cost+passingFees[v],nt,v))
        return -1
