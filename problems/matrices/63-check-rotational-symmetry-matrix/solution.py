class Solution:
    def hasRotationalSymmetry(self, grid: List[List[int]]) -> bool:
        m, n = len(grid), len(grid[0])
        for r in range((m + 1) // 2):
            mr = m - 1 - r
            col_limit = (n + 1) // 2 if r == mr else n
            for c in range(col_limit):
                if grid[r][c] != grid[mr][n - 1 - c]:
                    return False
        return True
