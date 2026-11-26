class Solution:
    def minimumSpanningTreeWeight(self, n: int, edges: List[List[int]]) -> int:
        if n <= 1:
            return 0

        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            if u != v:
                adj[u].append((w, v))
                adj[v].append((w, u))

        visited = [False] * n
        heap = [(0, 0)]
        total = 0
        visited_count = 0

        while heap and visited_count < n:
            w, u = heapq.heappop(heap)
            if visited[u]:
                continue
            visited[u] = True
            total += w
            visited_count += 1
            for nw, v in adj[u]:
                if not visited[v]:
                    heapq.heappush(heap, (nw, v))

        return total if visited_count == n else -1
