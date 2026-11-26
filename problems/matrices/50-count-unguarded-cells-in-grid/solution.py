class Solution:
    def countUnguarded(self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]) -> int:
        grid = [[0] * n for _ in range(m)]
        for r, c in guards:
            grid[r][c] = 1
        for r, c in walls:
            grid[r][c] = 2
        dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for r, c in guards:
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                while 0 <= nr < m and 0 <= nc < n:
                    cell = grid[nr][nc]
                    if cell == 1 or cell == 2:
                        break
                    grid[nr][nc] = 3
                    nr += dr
                    nc += dc
        ans = 0
        for row in grid:
            for v in row:
                if v == 0:
                    ans += 1
        return ans
