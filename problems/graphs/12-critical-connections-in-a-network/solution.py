class Solution:
    def criticalConnections(
        self, n: int, connections: List[List[int]]
    ) -> List[List[int]]:
        adj: List[List[int]] = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)

        disc = [-1] * n
        low = [0] * n
        bridges: List[List[int]] = []
        timer = 0

        for start in range(n):
            if disc[start] != -1:
                continue
            disc[start] = low[start] = timer
            timer += 1
            stack = [[start, -1, 0]]
            while stack:
                frame = stack[-1]
                u, parent, idx = frame[0], frame[1], frame[2]
                if idx < len(adj[u]):
                    frame[2] = idx + 1
                    v = adj[u][idx]
                    if v == parent:
                        continue
                    if disc[v] == -1:
                        disc[v] = low[v] = timer
                        timer += 1
                        stack.append([v, u, 0])
                    elif disc[v] < low[u]:
                        low[u] = disc[v]
                else:
                    stack.pop()
                    if parent != -1:
                        if low[u] < low[parent]:
                            low[parent] = low[u]
                        if low[u] > disc[parent]:
                            bridges.append([parent, u])

        return bridges
