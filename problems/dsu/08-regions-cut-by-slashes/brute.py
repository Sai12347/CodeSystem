class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)
        size = 3 * n
        mat = [[0] * size for _ in range(size)]
        for r in range(n):
            for c in range(n):
                ch = grid[r][c]
                br, bc = 3 * r, 3 * c
                if ch == "/":
                    mat[br][bc + 2] = 1
                    mat[br + 1][bc + 1] = 1
                    mat[br + 2][bc] = 1
                elif ch == "\\":
                    mat[br][bc] = 1
                    mat[br + 1][bc + 1] = 1
                    mat[br + 2][bc + 2] = 1

        regions = 0
        for r in range(size):
            for c in range(size):
                if mat[r][c] == 0:
                    regions += 1
                    q = deque([(r, c)])
                    mat[r][c] = 1
                    while q:
                        cr, cc = q.popleft()
                        for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                            if 0 <= nr < size and 0 <= nc < size and mat[nr][nc] == 0:
                                mat[nr][nc] = 1
                                q.append((nr, nc))
        return regions
