class Solution:
    def minimumCostWithDiscount(self, n: int, edges: List[List[int]], source: int, destination: int) -> int:
        graph=[[] for _ in range(n)]
        for u,v,w in edges: graph[u].append((v,w)); graph[v].append((u,w))
        inf=10**30; dist=[[inf,inf] for _ in range(n)]; dist[source][0]=0; heap=[(0,source,0)]
        while heap:
            d,u,used=heappop(heap)
            if d!=dist[u][used]: continue
            if u==destination: return d
            for v,w in graph[u]:
                if d+w<dist[v][used]: dist[v][used]=d+w; heappush(heap,(d+w,v,used))
                if not used and d+w//2<dist[v][1]: dist[v][1]=d+w//2; heappush(heap,(d+w//2,v,1))
        return -1
