class Solution:
    def largest1BorderedSquare(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        hor = [[0] * n for _ in range(m)]
        ver = [[0] * n for _ in range(m)]
        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    hor[r][c] = (hor[r][c - 1] if c > 0 else 0) + 1
                    ver[r][c] = (ver[r - 1][c] if r > 0 else 0) + 1
                    side = min(hor[r][c], ver[r][c])
                    while side > best:
                        if hor[r - side + 1][c] >= side and ver[r][c - side + 1] >= side:
                            best = side
                            break
                        side -= 1
        return best * best
