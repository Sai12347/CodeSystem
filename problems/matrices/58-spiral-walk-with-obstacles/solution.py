class Solution:
    def spiralWalkWithObstacles(self, grid: List[List[int]]) -> List[int]:
        m, n = len(grid), len(grid[0])
        dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
        vis = [[False] * n for _ in range(m)]
        r = c = d = 0
        vis[0][0] = True
        ans = [grid[0][0]]
        while True:
            moved = False
            for k in range(4):
                nd = (d + k) % 4
                nr = r + dirs[nd][0]
                nc = c + dirs[nd][1]
                if 0 <= nr < m and 0 <= nc < n and not vis[nr][nc] and grid[nr][nc] != -1:
                    r, c, d = nr, nc, nd
                    vis[r][c] = True
                    ans.append(grid[r][c])
                    moved = True
                    break
            if not moved:
                break
        return ans
