class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        adj = [[] for _ in range(n)]
        for i, (u, v, w) in enumerate(edges):
            adj[u].append((v, w, i))
            adj[v].append((u, w, i))

        INF = 10**18

        def prim(skip_idx: int = -1, force_idx: int = -1) -> int:
            visited = [False] * n
            heap = []
            total = 0
            count = 0

            if force_idx != -1:
                fu, fv, fw = edges[force_idx]
                visited[fu] = True
                visited[fv] = True
                total = fw
                count = 2
                for start in (fu, fv):
                    for nxt, w, idx in adj[start]:
                        if idx != force_idx and not visited[nxt]:
                            heapq.heappush(heap, (w, nxt))
            else:
                visited[0] = True
                count = 1
                for nxt, w, idx in adj[0]:
                    if idx != skip_idx:
                        heapq.heappush(heap, (w, nxt))

            while heap and count < n:
                w, u = heapq.heappop(heap)
                if visited[u]:
                    continue
                visited[u] = True
                total += w
                count += 1
                for nxt, nw, idx in adj[u]:
                    if idx != skip_idx and idx != force_idx and not visited[nxt]:
                        heapq.heappush(heap, (nw, nxt))

            return total if count == n else INF

        base = prim()
        critical = []
        pseudo = []
        for i in range(len(edges)):
            if prim(skip_idx=i) > base:
                critical.append(i)
            elif prim(force_idx=i) == base:
                pseudo.append(i)

        return [critical, pseudo]
