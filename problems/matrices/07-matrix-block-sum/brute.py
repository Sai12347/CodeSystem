class Solution:
    def matrixBlockSum(self, mat: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        ans = [[0] * n for _ in range(m)]
        for i in range(m):
            r1, r2 = max(0, i - k), min(m - 1, i + k)
            for j in range(n):
                c1, c2 = max(0, j - k), min(n - 1, j + k)
                s = 0
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        s += mat[r][c]
                ans[i][j] = s
        return ans
