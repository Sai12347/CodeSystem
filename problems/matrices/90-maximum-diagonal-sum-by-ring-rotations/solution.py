class Solution:
    def maxDiagonalSumAfterRingRotations(self, matrix: List[List[int]]) -> int:
        n = len(matrix)
        ans = matrix[n // 2][n // 2] if n % 2 == 1 else 0
        for k in range(n // 2):
            s = n - 1 - 2 * k
            best = None
            for i in range(s):
                cur = (
                    matrix[k][k + i]
                    + matrix[k + i][k + s]
                    + matrix[k + s][k + s - i]
                    + matrix[k + s - i][k]
                )
                if best is None or cur > best:
                    best = cur
            ans += best
        return ans
