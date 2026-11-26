class Solution:
    def numSubmatrixSumTarget(self, matrix: List[List[int]], target: int) -> int:
        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = [[matrix[r][c] for r in range(m)] for c in range(n)]
            m, n = n, m
        ans = 0
        for top in range(m):
            col_sums = [0] * n
            for bottom in range(top, m):
                row = matrix[bottom]
                freq = {0: 1}
                pref = 0
                for c in range(n):
                    col_sums[c] += row[c]
                    pref += col_sums[c]
                    ans += freq.get(pref - target, 0)
                    freq[pref] = freq.get(pref, 0) + 1
        return ans
