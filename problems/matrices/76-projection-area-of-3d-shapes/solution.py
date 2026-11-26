class Solution:
    def projectionArea(self, grid: List[List[int]]) -> int:
        n = len(grid)
        total = 0
        for i in range(n):
            row_max = 0
            col_max = 0
            for j in range(n):
                if grid[i][j] > 0:
                    total += 1
                if grid[i][j] > row_max:
                    row_max = grid[i][j]
                if grid[j][i] > col_max:
                    col_max = grid[j][i]
            total += row_max + col_max
        return total
