class Solution:
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        heights = [0] * n
        ans = 0
        for r in range(m):
            row = matrix[r]
            for c in range(n):
                heights[c] = heights[c] + 1 if row[c] == 1 else 0
            sorted_h = sorted(heights, reverse=True)
            for i, h in enumerate(sorted_h):
                if h == 0:
                    break
                area = h * (i + 1)
                if area > ans:
                    ans = area
        return ans
