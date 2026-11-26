class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            row = matrix[r]
            cur = self.prefix[r + 1]
            prev = self.prefix[r]
            for c in range(n):
                cur[c + 1] = row[c] + prev[c + 1] + cur[c] - prev[c]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        p = self.prefix
        return p[row2 + 1][col2 + 1] - p[row1][col2 + 1] - p[row2 + 1][col1] + p[row1][col1]
