class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res: List[List[str]] = []
        queens = [-1] * n
        full = (1 << n) - 1
        row_strs = ["." * c + "Q" + "." * (n - 1 - c) for c in range(n)]

        def backtrack(row: int, cols: int, d1: int, d2: int) -> None:
            if row == n:
                res.append([row_strs[c] for c in queens])
                return
            avail = full & ~(cols | d1 | d2)
            while avail:
                bit = avail & -avail
                avail ^= bit
                col = bit.bit_length() - 1
                queens[row] = col
                backtrack(row + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1)

        backtrack(0, 0, 0, 0)
        return res
