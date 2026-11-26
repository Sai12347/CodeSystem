class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        # Independent cross-check: Dijkstra with (cost, edges_used, node)
        # pruning only when a node was already popped with <= edges_used.
        adj = [[] for _ in range(n)]
        for u, v, p in flights:
            adj[u].append((v, p))

        min_edges = [k + 2] * n
        heap = [(0, 0, src)]
        while heap:
            cost, edges, u = heapq.heappop(heap)
            if u == dst:
                return cost
            if edges > k or edges >= min_edges[u]:
                continue
            min_edges[u] = edges
            for v, p in adj[u]:
                if edges + 1 < min_edges[v]:
                    heapq.heappush(heap, (cost + p, edges + 1, v))
        return -1
