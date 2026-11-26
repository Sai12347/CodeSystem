class Solution:
    def distanceLimitedPathsExist(
        self, n: int, edgeList: List[List[int]], queries: List[List[int]]
    ) -> List[bool]:
        adj = defaultdict(list)
        for u, v, w in edgeList:
            adj[u].append((v, w))
            adj[v].append((u, w))

        ans = []
        for p, q, limit in queries:
            visited = {p}
            dq = deque([p])
            found = False
            while dq:
                cur = dq.popleft()
                if cur == q:
                    found = True
                    break
                for nxt, w in adj[cur]:
                    if w < limit and nxt not in visited:
                        visited.add(nxt)
                        dq.append(nxt)
            ans.append(found)
        return ans
