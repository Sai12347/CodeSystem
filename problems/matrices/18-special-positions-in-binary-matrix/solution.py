class Solution:
    def numSpecial(self, mat: List[List[int]]) -> int:
        rows, cols = len(mat), len(mat[0])
        row_sum = [sum(row) for row in mat]
        col_sum = [sum(mat[r][c] for r in range(rows)) for c in range(cols)]
        return sum(mat[r][c] == 1 and row_sum[r] == 1 and col_sum[c] == 1 for r in range(rows) for c in range(cols))
