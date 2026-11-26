class Solution:
    def matrixScore(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        score = m * (1 << (n - 1))
        for c in range(1, n):
            same = sum(1 for r in range(m) if grid[r][c] == grid[r][0])
            score += max(same, m - same) * (1 << (n - 1 - c))
        return score
