class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        graph=[[] for _ in range(n)]
        for (u,v),p in zip(edges,succProb): graph[u].append((v,p)); graph[v].append((u,p))
        best=[0.0]*n; best[start]=1.0; heap=[(-1.0,start)]
        while heap:
            neg,u=heappop(heap); prob=-neg
            if prob < best[u]: continue
            if u==end: return prob
            for v,p in graph[u]:
                cand=prob*p
                if cand>best[v]: best[v]=cand; heappush(heap,(-cand,v))
        return 0.0
