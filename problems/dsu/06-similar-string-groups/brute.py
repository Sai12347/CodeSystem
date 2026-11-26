class Solution:
    def numSimilarGroups(self, strs: List[str]) -> int:
        n = len(strs)
        adj = [[] for _ in range(n)]
        for i in range(n):
            si = strs[i]
            for j in range(i + 1, n):
                sj = strs[j]
                diff = 0
                for ca, cb in zip(si, sj):
                    if ca != cb:
                        diff += 1
                        if diff > 2:
                            break
                if diff <= 2:
                    adj[i].append(j)
                    adj[j].append(i)

        visited = [False] * n
        groups = 0
        for i in range(n):
            if not visited[i]:
                groups += 1
                q = deque([i])
                visited[i] = True
                while q:
                    cur = q.popleft()
                    for nxt in adj[cur]:
                        if not visited[nxt]:
                            visited[nxt] = True
                            q.append(nxt)
        return groups
