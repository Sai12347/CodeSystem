class Solution:
    def numSubmat(self, mat: List[List[int]]) -> int:
        m, n = len(mat), len(mat[0])
        heights = [0] * n
        total = 0
        for r in range(m):
            for c in range(n):
                heights[c] = heights[c] + 1 if mat[r][c] == 1 else 0
            stack = []
            row_sum = [0] * n
            for c in range(n):
                while stack and heights[stack[-1]] >= heights[c]:
                    stack.pop()
                if stack:
                    prev = stack[-1]
                    row_sum[c] = row_sum[prev] + heights[c] * (c - prev)
                else:
                    row_sum[c] = heights[c] * (c + 1)
                stack.append(c)
                total += row_sum[c]
        return total
