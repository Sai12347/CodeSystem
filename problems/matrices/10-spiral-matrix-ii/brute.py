class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        mat = [[0] * n for _ in range(n)]
        dr = (0, 1, 0, -1)
        dc = (1, 0, -1, 0)
        r = c = d = 0
        for num in range(1, n * n + 1):
            mat[r][c] = num
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and mat[nr][nc] == 0:
                r, c = nr, nc
            else:
                d = (d + 1) % 4
                r, c = r + dr[d], c + dc[d]
        return mat
