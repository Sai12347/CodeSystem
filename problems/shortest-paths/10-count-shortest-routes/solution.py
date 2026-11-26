class Solution:
    def countShortestRoutes(self, n: int, roads: List[List[int]]) -> int:
        graph = [[] for _ in range(n)]
        for u, v, w in roads: graph[u].append((v,w)); graph[v].append((u,w))
        dist = [float('inf')] * n; ways = [0] * n; dist[0] = 0; ways[0] = 1
        heap = [(0,0)]; mod = 1000000007
        while heap:
            d,u = heappop(heap)
            if d != dist[u]: continue
            for v,w in graph[u]:
                nd = d + w
                if nd < dist[v]: dist[v] = nd; ways[v] = ways[u]; heappush(heap,(nd,v))
                elif nd == dist[v]: ways[v] = (ways[v] + ways[u]) % mod
        return ways[n-1]
