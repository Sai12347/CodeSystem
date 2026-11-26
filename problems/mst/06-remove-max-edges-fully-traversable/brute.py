class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        if n <= 1:
            return len(edges)

        def count_components(allowed_types):
            adj = [[] for _ in range(n + 1)]
            for t, u, v in edges:
                if t in allowed_types:
                    adj[u].append(v)
                    adj[v].append(u)
            visited = [False] * (n + 1)
            comps = 0
            for start in range(1, n + 1):
                if not visited[start]:
                    comps += 1
                    visited[start] = True
                    q = deque([start])
                    while q:
                        u = q.popleft()
                        for nxt in adj[u]:
                            if not visited[nxt]:
                                visited[nxt] = True
                                q.append(nxt)
            return comps

        if count_components({1, 3}) != 1 or count_components({2, 3}) != 1:
            return -1

        c3 = count_components({3})
        # Type 3 spanning forest uses (n - c3) edges; Alice and Bob each need (c3 - 1) more edges.
        min_needed = (n - c3) + 2 * (c3 - 1)
        return len(edges) - min_needed
