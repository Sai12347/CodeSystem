class Solution:
    def alternatingRingSpiral(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        res = []
        top, bottom, left, right = 0, m - 1, 0, n - 1
        layer = 0
        while top <= bottom and left <= right:
            if layer % 2 == 0:
                for c in range(left, right + 1):
                    res.append(matrix[top][c])
                for r in range(top + 1, bottom + 1):
                    res.append(matrix[r][right])
                if top < bottom:
                    for c in range(right - 1, left - 1, -1):
                        res.append(matrix[bottom][c])
                if left < right:
                    for r in range(bottom - 1, top, -1):
                        res.append(matrix[r][left])
            else:
                for r in range(top, bottom + 1):
                    res.append(matrix[r][left])
                if left < right:
                    for c in range(left + 1, right + 1):
                        res.append(matrix[bottom][c])
                if top < bottom and left < right:
                    for r in range(bottom - 1, top - 1, -1):
                        res.append(matrix[r][right])
                    for c in range(right - 1, left, -1):
                        res.append(matrix[top][c])
            top += 1
            bottom -= 1
            left += 1
            right -= 1
            layer += 1
        return res
