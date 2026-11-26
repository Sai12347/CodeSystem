class Solution:
    def maxHourglassSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        best = -10**18
        for r in range(m - 2):
            r0, r1, r2 = grid[r], grid[r + 1], grid[r + 2]
            for c in range(n - 2):
                s = r0[c] + r0[c + 1] + r0[c + 2] + r1[c + 1] + r2[c] + r2[c + 1] + r2[c + 2]
                if s > best:
                    best = s
        return best
