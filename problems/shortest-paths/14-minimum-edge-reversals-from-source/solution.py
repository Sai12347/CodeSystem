class Solution:
    def minimumReversalsFromSource(self, n: int, directedEdges: List[List[int]], source: int) -> List[int]:
        g=[[] for _ in range(n)]
        for u,v in directedEdges: g[u].append((v,0)); g[v].append((u,1))
        inf=10**9; dist=[inf]*n; dist[source]=0; heap=[(0,source)]
        while heap:
            d,u=heappop(heap)
            if d!=dist[u]:continue
            for v,w in g[u]:
                if d+w<dist[v]:dist[v]=d+w;heappush(heap,(d+w,v))
        return [-1 if x==inf else x for x in dist]
