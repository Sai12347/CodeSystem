class Solution:
    def bellmanFord(self, n: int, edges: List[List[int]], source: int) -> List[int]:
        inf=10**30; dist=[inf]*n; dist[source]=0
        for _ in range(n-1):
            changed=False
            for u,v,w in edges:
                if dist[u]!=inf and dist[u]+w<dist[v]: dist[v]=dist[u]+w; changed=True
            if not changed: break
        return [-1 if x==inf else x for x in dist]
