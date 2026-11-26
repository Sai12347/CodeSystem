class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        cols = len(matrix[0])
        heights = [0] * cols
        best = 0
        for row in matrix:
            for c in range(cols):
                heights[c] = heights[c] + 1 if row[c] == "1" else 0
            for i in range(cols):
                mn = heights[i]
                if mn == 0:
                    continue
                for j in range(i, cols):
                    if heights[j] < mn:
                        mn = heights[j]
                    if mn == 0:
                        break
                    area = mn * (j - i + 1)
                    if area > best:
                        best = area
        return best
