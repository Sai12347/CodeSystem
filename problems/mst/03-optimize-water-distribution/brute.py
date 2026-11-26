class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        adj = [[] for _ in range(n + 1)]
        for i, w in enumerate(wells, 1):
            adj[0].append((w, i))
            adj[i].append((w, 0))
        for u, v, cost in pipes:
            adj[u].append((cost, v))
            adj[v].append((cost, u))

        visited = [False] * (n + 1)
        heap = [(0, 0)]
        total = 0
        count = 0

        while heap and count <= n:
            cost, u = heapq.heappop(heap)
            if visited[u]:
                continue
            visited[u] = True
            total += cost
            count += 1
            for nc, v in adj[u]:
                if not visited[v]:
                    heapq.heappush(heap, (nc, v))

        return total
