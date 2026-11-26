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
            stack = []
            for i in range(cols + 1):
                cur = heights[i] if i < cols else 0
                while stack and heights[stack[-1]] > cur:
                    h = heights[stack.pop()]
                    left = stack[-1] if stack else -1
                    area = h * (i - left - 1)
                    if area > best:
                        best = area
                stack.append(i)
        return best
