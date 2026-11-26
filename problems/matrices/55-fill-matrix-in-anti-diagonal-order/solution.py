class Solution:
    def fillAntiDiagonal(self, rows: int, cols: int) -> List[List[int]]:
        res = [[0] * cols for _ in range(rows)]
        val = 1
        for d in range(rows + cols - 1):
            r_start = max(0, d - cols + 1)
            r_end = min(rows - 1, d)
            for r in range(r_start, r_end + 1):
                res[r][d - r] = val
                val += 1
        return res
