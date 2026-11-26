class Solution:
    def maxQuadrantSum(self, matrix: List[List[int]]) -> int:
        m = len(matrix)
        n = m // 2
        total = 0
        for r in range(n):
            mr = m - 1 - r
            for c in range(n):
                mc = m - 1 - c
                total += max(matrix[r][c], matrix[r][mc], matrix[mr][c], matrix[mr][mc])
        return total
