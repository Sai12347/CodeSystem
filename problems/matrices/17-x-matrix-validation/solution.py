class Solution:
    def checkXMatrix(self, matrix: List[List[int]]) -> int:
        n = len(matrix)
        for r in range(n):
            for c in range(n):
                diagonal = r == c or r + c == n - 1
                if diagonal == (matrix[r][c] == 0): return False
        return True
