class Solution:
    def maxSpiralSubarraySum(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        top, bottom, left, right = 0, m - 1, 0, n - 1
        started = False
        cur = 0
        best = 0

        def visit(v: int) -> None:
            nonlocal started, cur, best
            if not started:
                cur = best = v
                started = True
            else:
                cur = v if cur < 0 else cur + v
                if cur > best:
                    best = cur

        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                visit(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                visit(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    visit(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    visit(matrix[r][left])
                left += 1
        return best
