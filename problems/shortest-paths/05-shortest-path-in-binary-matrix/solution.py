class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return -1
        if n == 1:
            return 1

        visited = [[False] * n for _ in range(n)]
        visited[0][0] = True
        q = deque([(0, 0, 1)])
        dirs = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        )

        while q:
            r, c, dist = q.popleft()
            nd = dist + 1
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and not visited[nr][nc]:
                    if nr == n - 1 and nc == n - 1:
                        return nd
                    visited[nr][nc] = True
                    q.append((nr, nc, nd))

        return -1
