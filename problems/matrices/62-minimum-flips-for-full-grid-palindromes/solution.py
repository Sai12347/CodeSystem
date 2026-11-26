class Solution:
    def minFlipsFullPalindrome(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        flips = 0
        for r in range(m // 2):
            for c in range(n // 2):
                ones = (
                    grid[r][c]
                    + grid[r][n - 1 - c]
                    + grid[m - 1 - r][c]
                    + grid[m - 1 - r][n - 1 - c]
                )
                flips += min(ones, 4 - ones)

        diff = 0
        pair_ones = 0
        if m % 2 == 1:
            mr = m // 2
            for c in range(n // 2):
                a, b = grid[mr][c], grid[mr][n - 1 - c]
                if a != b:
                    diff += 1
                elif a == 1:
                    pair_ones += 1
        if n % 2 == 1:
            mc = n // 2
            for r in range(m // 2):
                a, b = grid[r][mc], grid[m - 1 - r][mc]
                if a != b:
                    diff += 1
                elif a == 1:
                    pair_ones += 1
        if m % 2 == 1 and n % 2 == 1 and grid[m // 2][n // 2] == 1:
            flips += 1

        flips += diff
        if pair_ones % 2 == 1 and diff == 0:
            flips += 2
        return flips
