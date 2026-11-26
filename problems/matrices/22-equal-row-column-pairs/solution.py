class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        columns = [tuple(grid[r][c] for r in range(len(grid))) for c in range(len(grid))]
        return sum(tuple(row) == col for row in grid for col in columns)
