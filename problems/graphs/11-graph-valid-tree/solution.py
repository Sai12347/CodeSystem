class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False

        adj: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = [False] * n
        visited[0] = True
        queue = deque([0])
        seen = 1

        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    seen += 1
                    queue.append(v)

        return seen == n
