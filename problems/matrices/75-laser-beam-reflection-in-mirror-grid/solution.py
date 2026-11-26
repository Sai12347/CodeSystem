class Solution:
    def illuminatedCells(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        dr = (0, 1, 0, -1)
        dc = (1, 0, -1, 0)
        seen = [[0] * n for _ in range(m)]
        r = c = d = 0
        lit = 0
        while 0 <= r < m and 0 <= c < n:
            bit = 1 << d
            if seen[r][c] & bit:
                break
            if seen[r][c] == 0:
                lit += 1
            seen[r][c] |= bit
            ch = grid[r][c]
            if ch == '/':
                d = 3 - d
            elif ch == '\\':
                d ^= 1
            r += dr[d]
            c += dc[d]
        return lit
