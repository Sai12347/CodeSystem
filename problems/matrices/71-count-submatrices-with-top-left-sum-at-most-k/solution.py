class Solution:
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        n = len(grid[0])
        col_sum = [0] * n
        ans = 0
        for row in grid:
            cur = 0
            for c in range(n):
                col_sum[c] += row[c]
                cur += col_sum[c]
                if cur <= k:
                    ans += 1
                else:
                    break
        return ans
