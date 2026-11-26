class Solution:
    def concentricRingSums(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        top, bottom, left, right = 0, m - 1, 0, n - 1
        res = []
        while top <= bottom and left <= right:
            s = 0
            for c in range(left, right + 1):
                s += matrix[top][c]
            if bottom > top:
                for c in range(left, right + 1):
                    s += matrix[bottom][c]
            for r in range(top + 1, bottom):
                s += matrix[r][left]
                if right > left:
                    s += matrix[r][right]
            res.append(s)
            top += 1
            bottom -= 1
            left += 1
            right -= 1
        return res
