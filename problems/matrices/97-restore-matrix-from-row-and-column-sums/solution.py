class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        m, n = len(rowSum), len(colSum)
        r_rem = rowSum[:]
        c_rem = colSum[:]
        ans = [[0] * n for _ in range(m)]
        r = c = 0
        while r < m and c < n:
            val = r_rem[r] if r_rem[r] < c_rem[c] else c_rem[c]
            ans[r][c] = val
            r_rem[r] -= val
            c_rem[c] -= val
            if r_rem[r] == 0:
                r += 1
            if c_rem[c] == 0:
                c += 1
        return ans
