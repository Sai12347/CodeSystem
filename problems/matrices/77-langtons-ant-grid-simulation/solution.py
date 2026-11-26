class Solution:
    def simulateLangtonsAnt(self, grid: List[List[int]], startRow: int, startCol: int, steps: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        res = [row[:] for row in grid]
        dr = (-1, 0, 1, 0)
        dc = (0, 1, 0, -1)
        r, c, d = startRow, startCol, 0
        for _ in range(steps):
            if res[r][c] == 0:
                d = (d + 1) % 4
                res[r][c] = 1
            else:
                d = (d + 3) % 4
                res[r][c] = 0
            r += dr[d]
            c += dc[d]
            if r < 0 or r >= m or c < 0 or c >= n:
                break
        return res
