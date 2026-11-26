class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = [False] * n
        components = 0
        for i in range(n):
            if not visited[i]:
                components += 1
                q = deque([i])
                visited[i] = True
                while q:
                    cur = q.popleft()
                    for nxt in adj[cur]:
                        if not visited[nxt]:
                            visited[nxt] = True
                            q.append(nxt)
        return components
