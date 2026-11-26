class Solution:
    def largestEqualZeroOneSubmatrix(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if m > n:
            grid = [[grid[r][c] for r in range(m)] for c in range(n)]
            m, n = n, m
        best = 0
        for r1 in range(m):
            col = [0] * n
            for r2 in range(r1, m):
                height = r2 - r1 + 1
                row = grid[r2]
                prefix = 0
                first = {0: -1}
                for c in range(n):
                    col[c] += 1 if row[c] == 1 else -1
                    prefix += col[c]
                    if prefix in first:
                        area = height * (c - first[prefix])
                        if area > best:
                            best = area
                    else:
                        first[prefix] = c
        return best
