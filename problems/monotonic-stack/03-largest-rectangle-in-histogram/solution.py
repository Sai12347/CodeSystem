class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        best = 0
        n = len(heights)
        for i in range(n + 1):
            cur = heights[i] if i < n else 0
            while stack and heights[stack[-1]] > cur:
                h = heights[stack.pop()]
                left = stack[-1] if stack else -1
                area = h * (i - left - 1)
                if area > best:
                    best = area
            stack.append(i)
        return best
