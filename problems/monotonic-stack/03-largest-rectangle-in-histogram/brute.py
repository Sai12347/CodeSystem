class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        n = len(heights)
        best = 0
        for i in range(n):
            mn = heights[i]
            for j in range(i, n):
                if heights[j] < mn:
                    mn = heights[j]
                area = mn * (j - i + 1)
                if area > best:
                    best = area
        return best
