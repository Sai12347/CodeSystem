class Solution:
    def checkValidKnightTour(self, grid: List[List[int]]) -> bool:
        n = len(grid)
        if grid[0][0] != 0:
            return False
        moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        r, c = 0, 0
        for step in range(1, n * n):
            found = False
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == step:
                    r, c = nr, nc
                    found = True
                    break
            if not found:
                return False
        return True
