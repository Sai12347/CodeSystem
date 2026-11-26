class Solution:
    def rotateMatrix(self, matrix: List[List[int]], rotations: int) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        k = rotations % 4
        if k == 0:
            return [row[:] for row in matrix]
        if k == 1:
            return [[matrix[m - 1 - r][c] for r in range(m)] for c in range(n)]
        if k == 2:
            return [[matrix[m - 1 - r][n - 1 - c] for c in range(n)] for r in range(m)]
        return [[matrix[r][n - 1 - c] for r in range(m)] for c in range(n)]
