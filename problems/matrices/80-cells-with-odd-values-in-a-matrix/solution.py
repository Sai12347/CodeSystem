class Solution:
    def oddCells(self, m: int, n: int, indices: List[List[int]]) -> int:
        row_odd = [0] * m
        col_odd = [0] * n
        for r, c in indices:
            row_odd[r] ^= 1
            col_odd[c] ^= 1
        ro = sum(row_odd)
        co = sum(col_odd)
        return ro * (n - co) + (m - ro) * co
