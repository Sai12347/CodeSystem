class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        cur = [row[:] for row in grid]
        minutes = 0

        while True:
            to_rot = []
            for r in range(rows):
                for c in range(cols):
                    if cur[r][c] == 1:
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and cur[nr][nc] == 2:
                                to_rot.append((r, c))
                                break
            if not to_rot:
                break
            for r, c in to_rot:
                cur[r][c] = 2
            minutes += 1

        for r in range(rows):
            for c in range(cols):
                if cur[r][c] == 1:
                    return -1
        return minutes
