class Solution:
    def candyCrush(self, board: List[List[int]]) -> List[List[int]]:
        m, n = len(board), len(board[0])
        g = [row[:] for row in board]
        while True:
            crush = [[False] * n for _ in range(m)]
            changed = False
            for r in range(m):
                for c in range(n - 2):
                    v = g[r][c]
                    if v != 0 and v == g[r][c + 1] == g[r][c + 2]:
                        crush[r][c] = crush[r][c + 1] = crush[r][c + 2] = True
                        changed = True
            for c in range(n):
                for r in range(m - 2):
                    v = g[r][c]
                    if v != 0 and v == g[r + 1][c] == g[r + 2][c]:
                        crush[r][c] = crush[r + 1][c] = crush[r + 2][c] = True
                        changed = True
            if not changed:
                return g
            for c in range(n):
                write = m - 1
                for r in range(m - 1, -1, -1):
                    if not crush[r][c] and g[r][c] != 0:
                        g[write][c] = g[r][c]
                        write -= 1
                while write >= 0:
                    g[write][c] = 0
                    write -= 1
