class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        if n <= 1:
            return 0
        adj = [[] for _ in range(n + 1)]
        for u, v, w in connections:
            adj[u].append((w, v))
            adj[v].append((w, u))

        visited = [False] * (n + 1)
        heap = [(0, 1)]
        total = 0
        count = 0

        while heap and count < n:
            w, u = heapq.heappop(heap)
            if visited[u]:
                continue
            visited[u] = True
            total += w
            count += 1
            for nw, v in adj[u]:
                if not visited[v]:
                    heapq.heappush(heap, (nw, v))

        return total if count == n else -1
