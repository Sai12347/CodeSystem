class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        copy = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                copy[c][n - 1 - r] = matrix[r][c]
        for r in range(n):
            for c in range(n):
                matrix[r][c] = copy[r][c]
