class Solution:
    def criticalConnections(
        self, n: int, connections: List[List[int]]
    ) -> List[List[int]]:
        # Brute force: remove each edge and test if node 0 can still reach all n nodes.
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)

        bridges = []
        for skip_u, skip_v in connections:
            visited = [False] * n
            visited[0] = True
            q = deque([0])
            count = 1
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if (u == skip_u and v == skip_v) or (u == skip_v and v == skip_u):
                        continue
                    if not visited[v]:
                        visited[v] = True
                        count += 1
                        q.append(v)
            if count < n:
                bridges.append([skip_u, skip_v])
        return bridges
