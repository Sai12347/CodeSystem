class Solution:
    def sumMatrixBorder(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        return sum(matrix[r][c] for r in range(m) for c in range(n) if r == 0 or r == m-1 or c == 0 or c == n-1)
