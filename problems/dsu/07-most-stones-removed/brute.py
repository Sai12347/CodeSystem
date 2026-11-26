class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        n = len(stones)
        adj = [[] for _ in range(n)]
        for i in range(n):
            ri, ci = stones[i]
            for j in range(i + 1, n):
                if stones[j][0] == ri or stones[j][1] == ci:
                    adj[i].append(j)
                    adj[j].append(i)

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
        return n - components
