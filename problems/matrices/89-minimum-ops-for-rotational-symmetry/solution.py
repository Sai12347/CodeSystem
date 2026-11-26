class Solution:
    def minOpsRotationalSymmetry(self, grid: List[List[int]]) -> int:
        n = len(grid)
        ops = 0
        for r in range(n // 2):
            for c in range((n + 1) // 2):
                vals = [
                    grid[r][c],
                    grid[c][n - 1 - r],
                    grid[n - 1 - r][n - 1 - c],
                    grid[n - 1 - c][r],
                ]
                vals.sort()
                ops += (vals[3] - vals[0]) + (vals[2] - vals[1])
        return ops
