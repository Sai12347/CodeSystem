class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        # Independent cross-check: Dijkstra with Chebyshev heuristic (A*)
        n = len(grid)
        if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return -1
        inf = 10**9
        dist = [[inf] * n for _ in range(n)]
        dist[0][0] = 1
        heap = [(1 + max(n - 1, n - 1), 1, 0, 0)]

        while heap:
            _, d, r, c = heapq.heappop(heap)
            if d > dist[r][c]:
                continue
            if r == n - 1 and c == n - 1:
                return d
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                        nd = d + 1
                        if nd < dist[nr][nc]:
                            dist[nr][nc] = nd
                            h = max(n - 1 - nr, n - 1 - nc)
                            heapq.heappush(heap, (nd + h, nd, nr, nc))
        return -1
