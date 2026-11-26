class Solution:
    def largestMagicSquare(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        row_pref = [[0] * (n + 1) for _ in range(m)]
        col_pref = [[0] * n for _ in range(m + 1)]
        for r in range(m):
            for c in range(n):
                row_pref[r][c + 1] = row_pref[r][c] + grid[r][c]
                col_pref[r + 1][c] = col_pref[r][c] + grid[r][c]

        for k in range(min(m, n), 1, -1):
            for r in range(m - k + 1):
                for c in range(n - k + 1):
                    target = row_pref[r][c + k] - row_pref[r][c]
                    ok = True
                    for i in range(1, k):
                        if row_pref[r + i][c + k] - row_pref[r + i][c] != target:
                            ok = False
                            break
                    if not ok:
                        continue
                    for j in range(k):
                        if col_pref[r + k][c + j] - col_pref[r][c + j] != target:
                            ok = False
                            break
                    if not ok:
                        continue
                    d1 = d2 = 0
                    for i in range(k):
                        d1 += grid[r + i][c + i]
                        d2 += grid[r + i][c + k - 1 - i]
                    if d1 == target and d2 == target:
                        return k
        return 1
