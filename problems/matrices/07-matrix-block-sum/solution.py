class Solution:
    def matrixBlockSum(self, mat: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        pref = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            row_sum = 0
            for c in range(n):
                row_sum += mat[r][c]
                pref[r + 1][c + 1] = pref[r][c + 1] + row_sum
        ans = [[0] * n for _ in range(m)]
        for r in range(m):
            r1 = max(0, r - k)
            r2 = min(m - 1, r + k)
            for c in range(n):
                c1 = max(0, c - k)
                c2 = min(n - 1, c + k)
                ans[r][c] = (
                    pref[r2 + 1][c2 + 1]
                    - pref[r1][c2 + 1]
                    - pref[r2 + 1][c1]
                    + pref[r1][c1]
                )
        return ans
