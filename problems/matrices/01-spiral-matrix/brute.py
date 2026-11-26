class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        seen = [[False] * n for _ in range(m)]
        dr = (0, 1, 0, -1)
        dc = (1, 0, -1, 0)
        r = c = d = 0
        res = []
        for _ in range(m * n):
            res.append(matrix[r][c])
            seen[r][c] = True
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc]:
                r, c = nr, nc
            else:
                d = (d + 1) % 4
                r, c = r + dr[d], c + dc[d]
        return res
