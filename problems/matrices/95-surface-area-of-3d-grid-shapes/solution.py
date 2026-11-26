class Solution:
    def surfaceArea(self, grid: List[List[int]]) -> int:
        n = len(grid)
        area = 0
        for r in range(n):
            for c in range(n):
                v = grid[r][c]
                if v > 0:
                    area += 4 * v + 2
                    if r > 0:
                        area -= 2 * min(v, grid[r - 1][c])
                    if c > 0:
                        area -= 2 * min(v, grid[r][c - 1])
        return area
