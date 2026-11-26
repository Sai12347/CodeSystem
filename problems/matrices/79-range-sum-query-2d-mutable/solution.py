class NumMatrix2D:
    def __init__(self, matrix: List[List[int]]):
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.vals = [[0] * self.n for _ in range(self.m)]
        self.bit = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        for r in range(self.m):
            for c in range(self.n):
                self.update(r, c, matrix[r][c])

    def update(self, row: int, col: int, val: int) -> None:
        delta = val - self.vals[row][col]
        self.vals[row][col] = val
        i = row + 1
        while i <= self.m:
            j = col + 1
            row_bit = self.bit[i]
            while j <= self.n:
                row_bit[j] += delta
                j += j & -j
            i += i & -i

    def _prefix(self, r: int, c: int) -> int:
        total = 0
        i = r
        while i > 0:
            j = c
            row_bit = self.bit[i]
            while j > 0:
                total += row_bit[j]
                j -= j & -j
            i -= i & -i
        return total

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self._prefix(row2 + 1, col2 + 1)
            - self._prefix(row1, col2 + 1)
            - self._prefix(row2 + 1, col1)
            + self._prefix(row1, col1)
        )
