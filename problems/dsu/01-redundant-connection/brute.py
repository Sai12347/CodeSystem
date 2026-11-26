class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        adj = [[] for _ in range(n + 1)]
        for idx, (u, v) in enumerate(edges):
            adj[u].append((v, idx))
            adj[v].append((u, idx))

        for skip in range(n - 1, -1, -1):
            seen = [False] * (n + 1)
            q = deque([1])
            seen[1] = True
            count = 1
            while q:
                cur = q.popleft()
                for nxt, eidx in adj[cur]:
                    if eidx == skip or seen[nxt]:
                        continue
                    seen[nxt] = True
                    count += 1
                    q.append(nxt)
            if count == n:
                return edges[skip]
        return []
